from datetime import datetime

from bbbapi.controller.sensor_werte_list_controller import \
    SensorWertListController
from bbbapi.models.sensor import Sensor

from bbbapi.common_types import Roles
from tedious.mdl.list_controller import ListController
from tedious.res.list_resource import ListResource


class SensorWertListResource(ListResource):
    """Erstellt eine Auflistung von allen Werten eines Sensors."""

    def __init__(self, sensor: Sensor, limit=25):
        self.sensor = sensor
        super().__init__([
            Roles.ADMIN.value,
            Roles.PERSONAL.value
        ], [
            'id', 'dekodiertJSON', 'erhalten'
        ], limit,
            True)

    async def get_controller(self, request, **kwargs) -> ListController:

        datetime_min = datetime.fromtimestamp(float(request.get_param('min')))
        datetime_max = datetime.fromtimestamp(float(request.get_param('max')))

        return SensorWertListController(self.sensor, datetime_min, datetime_max)