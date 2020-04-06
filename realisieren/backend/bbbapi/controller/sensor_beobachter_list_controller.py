from bbbapi.models.sensor import Sensor
from bbbapi.models.beobachter import Beobachter
from tedious.mdl.list_controller import ListController


class SensorBeobachterListController(ListController):
    """Erstellt eine Auflistung von allen Beobachtern eines Sensors."""

    def __init__(self, sensor: Sensor):
        super().__init__(Beobachter)
        self.sensor = sensor

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

       return """
            SELECT id, art, name, ausloeserWert as "ausloeserWert", stand, wertName as "wertName" from beobachter WHERE dev_euisensor=$1
       """

    async def _select_values(self):
        return self.sensor["dev_eui"].value,