from bbbapi.controller.sensor_beobachter_list_controller import \
    SensorBeobachterListController
from bbbapi.models.sensor import Sensor

from bbbapi.common_types import Roles
from tedious.mdl.list_controller import ListController
from tedious.res.list_resource import ListResource

class SensorBeobachterListResource(ListResource):
    """Erstellt eine Auflistung von allen Beobachtern eines Sensors."""

    def __init__(self, sensor: Sensor, limit=25):
        self.sensor = sensor
        super().__init__([
            Roles.ADMIN.value,
            Roles.PERSONAL.value
        ], [
            'id', 'art', 'name', 'ausloeserWert', 'wertName', 'stand'
        ], limit,
            True)

    async def get_controller(self, request, **kwargs) -> ListController:
        return SensorBeobachterListController(self.sensor)