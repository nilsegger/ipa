from typing import Dict, Any
from bbbapi.decoders.decoder import Decoder
from bbbapi.common_types import SensorArt


class TabsDecoder(Decoder):
    """Dekodiert einen Wert eines Tabs Sensors anhand dieses `Datenblatts
    <https://iot-shop.de/wp-content/uploads/2020/03/RM_Door-_-Window-Sensor_20200205_v2.pdf>`__
    """

    def __init__(self):
        super().__init__(SensorArt.TABS)

    async def decode(self, data: str) -> Dict[str, Any]:
        """Dekodiert den Sensor Wert in folgende Werte.

            - Status
            - Batterie Spannung

        Args:
            data (str): Sensor Wert in Hex.

        Returns:
            Ein Dict, welches die Oben gennanten Werte enthölt.
        """

        status_bits = data[0:2]
        # if status is True, door is open
        status = bin(int(status_bits, base=16))[-1] == '1'

        battery = int(data[3], base=16)

        return {
            'status': status,
            'vdd': int(100 / 14 * battery)
        }
