from bbbapi.models.sensor import Sensor
from tedious.mdl.list_controller import ListController

from bbbapi.models.sensor_wert import SensorWert


class SensorWertListController(ListController):
    """Erstellt eine Auflistung von allen Werten eines Sensors."""

    def __init__(self, sensor: Sensor, datetime_min, datetime_max):
        super().__init__(SensorWert)
        self.sensor = sensor
        self.datetime_min = datetime_min
        self.datetime_max = datetime_max

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

       return """
            SELECT id, dekodiertJSON as "dekodiertJSON", erhalten from sensorenwerte WHERE dev_euisensor=$1 AND erhalten >= $2 AND erhalten <= $3 ORDER BY erhalten ASC
       """

    async def _select_values(self):
        return self.sensor["dev_eui"].value, self.datetime_min, self.datetime_max