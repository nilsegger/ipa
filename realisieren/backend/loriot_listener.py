import tedious.config
from bbbapi.decoders.tabs import TabsDecoder
from bbbapi.decoders.elsys import ElsysDecoder
from bbbapi.decoders.adeunis import AdeunisDecoder
from bbbapi.common_types import SensorArt
from bbbapi.models.sensor import Sensor, datetime
import time
from bbbapi.controller.sensor_controller import SensorController
from tedious.sql.postgres import PostgreSQLDatabase, Connection
import asyncio
import websockets
import json

tedious.config.load_config('config.ini')

continue_listening = True

sensor_controller = SensorController()

decoders = {
    SensorArt.ADEUNIS_RF: AdeunisDecoder(),
    SensorArt.ELSYS_ERS_CO2: ElsysDecoder(),
    SensorArt.TABS: TabsDecoder()
}


async def lookup_sensor(connection: Connection, dev_eui: str):
    """Sucht in der Sensoren Tabllen nach dem Sensor mit der dev_eui.

    Args:
        connection: Verbindung zur Datenbank.
        dev_eui: ID des Sensors.

    Returns:
        Sensor Modell falls dieses existiert, sont None
    """
    sensor = Sensor(dev_eui=dev_eui)
    if await sensor_controller.get(connection, sensor) is not None:
        return sensor
    else:
        return None


async def handle(connection: Connection, sensor: Sensor, raw, decoded):
    """Lädt die neuen Sensor Daten in die SensorWert Tabelle und alarmiert Beobachter.

    Args:
        connection: Verbindung zur Datenbank
        sensor: Sensor Modell
        raw: Roher Sensor Wert
        decoded: Dekodierter Sensor Wert in form eines Dict
    """
    stmt = "INSERT INTO sensorenwerte (dev_euisensor, rohwert, dekodiertjson, erhalten) VALUES ($1, $2, $3, $4)"
    await connection.execute(stmt, sensor["dev_eui"].value, raw,
                             json.dumps(decoded), datetime.now())


async def listen(uri: str, db: PostgreSQLDatabase):
    """Hört uri mit websockets ab. Wenn ein Wert empfangen wird, wird die dev_eui
    in der Sensoren Tabelle gesucht, falls diese existiert, wird der Wert in die SensorenWerte Tabelle geschrieben.
    Falls der Sensor einen oder mehrere Beobachter angehängt hat, so werden diese vom erhaltenen Wert alamiert.

    Args:
        uri: URI zu welcher die Verbinung mit Websockets aufgebaut wird.
        db: Datenbank von welcher die Sensoren ausgelesen werden kann
    """
    async with websockets.connect(uri) as websocket:

        while continue_listening:
            message = await websocket.recv()
            payload = json.loads(message)

            # identifies type of message, rx = uplink message
            if payload["cmd"] == "rx" and 'data' in payload:
                dev_eui = payload['EUI']
                raw = payload['data']

                async with await db.acquire() as connection:
                    sensor = await lookup_sensor(connection, dev_eui)
                    if sensor is not None:
                        if sensor["art"].value not in decoders:
                            print(
                                "Überspringe Sensor der Art {}, da kein Dekodierer existiert.".format(
                                    sensor["art"].value))
                        else:
                            decoded = await decoders[
                                sensor["art"].value].decode(raw)
                            await handle(connection, sensor, raw,
                                         decoded)
                    else:
                        print(
                            "Sensor {} übersprungen da dieser nicht eingetragen ist.".format(
                                dev_eui))


async def main():
    """Öffnet Verbindung zu Loriot und versucht diese am Leben zu halten. Wird eine Exception erhoben, so wird 5 Sekunden gewartet bis wieder Verbunden wird."""

    token = tedious.config.CONFIG["LORIOT"]['token']
    uri = tedious.config.CONFIG["LORIOT"]['uri'].format(token)

    async with PostgreSQLDatabase(
            **tedious.config.CONFIG["DB_CREDENTIALS"]) as db:
        while True:
            try:
                print("{} Server gestartet.".format(datetime.now()))
                await listen(uri, db)
            except Exception as e:
                print(
                    "{} Eine Exception wurde erhoben. Es werden 5s gewartet bis der Server wieder gestartet wird. \n {} {}".format(
                        datetime.now(), type(e), str(e)))
                time.sleep(5)


"""
async def add_sensor():
    async with PostgreSQLDatabase(
            **tedious.config.CONFIG["DB_CREDENTIALS"]) as db:
        async with await db.acquire() as connection:
            sensor = Sensor(dev_eui="0018B20000001CD0")
            sensor["name"].value = "Adeunis Test Sensor"
            sensor["art"].value = SensorTypes.ADEUNIS_RF
            sensor["raum"]["id"].value = 3
            await sensor_controller.create(connection, sensor)
"""

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
