import tedious.config
from bbbapi.controller.beobachter_controller import BeobachterController

from bbbapi.models.beobachter import Beobachter

from bbbapi.beobachter.beobachter import ZaehlerstandBeobachter
from bbbapi.common_types import SensorArt, BeobachterArt

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

async def main():
    """Erstellt den Adeunis Sensor und fügt einen Beobachter hinzu."""

    tedious.config.load_config('config.ini')

    db = PostgreSQLDatabase(**tedious.config.CONFIG["DB_CREDENTIALS"])

    async with db:
        async with await db.acquire() as connection:
            gebaeude = Gebaeude()
            gebaeude["name"].value = "Bruggerstrasse"
            await GebaeudeController().create(connection, gebaeude)
            stockwerk = Stockwerk()
            stockwerk["gebaeude"]["id"].value = gebaeude["id"].value
            stockwerk["name"].value = "Erdgeschoss"
            stockwerk["niveau"].value = 0
            await StockwerkController().create(connection, stockwerk)
            raum = Raum()
            raum["name"].value = "Zimmer 512"
            raum["stockwerk"]["id"].value = stockwerk["id"].value
            await RaumController().create(connection, raum)

            adeunis = Sensor(dev_eui="0018B20000001CD0")
            adeunis["name"].value = "Adeunis Test Sensor"
            adeunis["art"].value = SensorArt.ADEUNIS_RF
            adeunis["raum"]["id"].value = raum["id"].value
            await SensorController().create(connection, adeunis)

            beobachter = Beobachter()
            beobachter["name"].value = "Zählerstand Beobachter"
            beobachter["art"].value = BeobachterArt.ZAEHLERSTAND
            beobachter["ausloeserWert"].value = 10
            beobachter["sensor"]["dev_eui"].value = adeunis["dev_eui"].value

            await BeobachterController().create(connection, beobachter)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())