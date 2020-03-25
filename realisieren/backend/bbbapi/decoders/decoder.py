from bbbapi.common_types import SensorTypes
from typing import Dict, Any


class Decoder:
    """Interface Klasse für Sensor Wert Dekodierer."""

    __slots__ = ('sensor_type', )

    def __init__(self, sensor_type: SensorTypes):
        self.sensor_type = sensor_type

    async def decode(self, data: str) -> Dict[str, Any]:
        """Dekodiert den Wert eines Sensors des Types `self.sensor_type`.

        Args:
            data (str): Daten des Sensor.

        Returns:
            Ein Dict welches die verschiedenen Werte entzogen von `data`
            enthält.
        """
        raise NotImplementedError
