import tedious.config
from bbbapi.controller.material_controller import MaterialController

from bbbapi.models.material import Material

from bbbapi.controller.personal_controller import PersonalController

from bbbapi.models.personal import Personal

from bbbapi.controller.beobachter_controller import BeobachterController

from bbbapi.models.beobachter import Beobachter

from bbbapi.beobachter.beobachter import ZaehlerstandBeobachter
from bbbapi.common_types import SensorArt, BeobachterArt, Roles

from bbbapi.controller.raum_controller import RaumController

from bbbapi.controller.stockwerk_controller import StockwerkController
from bbbapi.controller.gebaeude_controller import GebaeudeController
from bbbapi.models.gebaeude import Gebaeude
from bbbapi.models.stockwerk import Stockwerk
from bbbapi.models.raum import Raum
from bbbapi.models.sensor import Sensor
from bbbapi.controller.sensor_controller import SensorController
from tedious.sql.postgres import PostgreSQLDatabase
import asyncio


async def create_stockwerk(connection, name, niveau, gebaeude_id):
    stockwerk = Stockwerk()
    stockwerk["gebaeude"]["id"].value = gebaeude_id
    stockwerk["name"].value = name
    stockwerk["niveau"].value = niveau
    return await StockwerkController().create(connection, stockwerk)


async def create_raum(connection, name, stockwerk_id):
    raum = Raum()
    raum["name"].value = name
    raum["stockwerk"]["id"].value = stockwerk_id
    return await RaumController().create(connection, raum)


async def create_sensor(connection, dev_eui, name, art, raum_id):
    sensor = Sensor(dev_eui=dev_eui)
    sensor["name"].value = name
    sensor["art"].value = art
    sensor["raum"]["id"].value = raum_id
    return await SensorController().create(connection, sensor)


async def create_beobachter(connection, name, art, ausloeserWert,
                            sensor_dev_eui, wertName=None):
    beobachter = Beobachter()
    beobachter["name"].value = name
    beobachter["art"].value = art
    beobachter["ausloeserWert"].value = ausloeserWert
    beobachter["wertName"].value = wertName
    beobachter["sensor"]["dev_eui"].value = sensor_dev_eui
    return await BeobachterController().create(connection, beobachter)


async def create_material(connection, name):
    material = Material()
    material["name"].value = name
    return await MaterialController().create(connection, material)


async def add_material_to_beobachter(connection, material, beobachter):
    await BeobachterController().add_material(connection, beobachter, material)

async def main():
    """Erstellt den Adeunis Sensor und fügt einen Beobachter hinzu."""

    tedious.config.load_config('config.ini')

    db = PostgreSQLDatabase(**tedious.config.CONFIG["DB_CREDENTIALS"])

    async with db:
        async with await db.acquire() as connection:
            model = Personal()
            model['name'].value = 'Administrator'
            model['benutzername'].value = 'admin'
            model['passwort'].value = '12345678'
            model['rolle'].value = Roles.ADMIN
            await PersonalController().create(connection, model)

            gebaeude = Gebaeude()
            gebaeude["name"].value = "Bruggerstrasse"
            await GebaeudeController().create(connection, gebaeude)

            erdgeschoss = await create_stockwerk(connection, 'Erdgeschoss', 0,
                                                 gebaeude["id"].value)
            obergeschoss = await create_stockwerk(connection, 'Obergeschoss',
                                                  1, gebaeude["id"].value)

            raum_1 = await create_raum(connection, "Zimmer 1",
                                       erdgeschoss["id"].value)
            raum_2 = await create_raum(connection, "Zimmer 2",
                                       erdgeschoss["id"].value)
            raum_3 = await create_raum(connection, "Zimmer 10",
                                       obergeschoss["id"].value)

            adeunis = await create_sensor(connection, "0018B20000001CD0",
                                          "Adeunis Sensor",
                                          SensorArt.ADEUNIS_RF,
                                          raum_1["id"].value)
            elsys1 = await create_sensor(connection, "A81758FFFE048EDE",
                                         "Elsys Sensor 1",
                                         SensorArt.ELSYS_ERS_CO2,
                                         raum_2["id"].value)
            elsys2 = await create_sensor(connection, "A81758FFFE048CCA",
                                         "Elsys Sensor 1",
                                         SensorArt.ELSYS_ERS_CO2,
                                         raum_3["id"].value)

            await create_beobachter(connection, 'Adeunis Temperatur Darüber',
                                    BeobachterArt.RICHTWERT_DARUEBER, 25,
                                    adeunis["dev_eui"].value, wertName='temperature')
            await create_beobachter(connection, 'Adeunis Temperatur Darunter',
                                    BeobachterArt.RICHTWERT_DARUNTER, 18,
                                    adeunis["dev_eui"].value, wertName='temperature')
            adeunis_zaehlerstand_beobachter = await create_beobachter(connection, 'Adeunis Zählerstand',
                                    BeobachterArt.ZAEHLERSTAND, 3,
                                    adeunis["dev_eui"].value)

            seife = await create_material(connection, 'Seife')
            await add_material_to_beobachter(connection, seife, adeunis_zaehlerstand_beobachter)

            wc_papier = await create_material(connection, 'WC Papier')
            await add_material_to_beobachter(connection, wc_papier, adeunis_zaehlerstand_beobachter)

            await create_beobachter(connection, 'Elsys Temperatur Darüber',
                                    BeobachterArt.RICHTWERT_DARUEBER, 25,
                                    elsys1["dev_eui"].value, wertName='temperature')
            await create_beobachter(connection, 'Elsys CO2 Darüber',
                                    BeobachterArt.RICHTWERT_DARUEBER, 600,
                                    elsys1["dev_eui"].value ,wertName='co2')

            await create_beobachter(connection, 'Elsys Temperatur Darüber',
                                    BeobachterArt.RICHTWERT_DARUEBER, 25,
                                    elsys2["dev_eui"].value, wertName='temperature')
            await create_beobachter(connection, 'Elsys CO2 Darüber',
                                    BeobachterArt.RICHTWERT_DARUEBER, 600,
                                    elsys2["dev_eui"].value, wertName='co2')



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
