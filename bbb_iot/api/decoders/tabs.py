from typing import Dict, Any
from decoders.decoder import Decoder


class TabsDecoder(Decoder):
    """Dekodiert einen Wert eines Tabs Sensors anhand dieses `Datenblatts
    <https://iot-shop.de/wp-content/uploads/2020/03/RM_Door-_-Window-Sensor_20200205_v2.pdf>`__
    """

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

        battery_bits = bin(int(data[2:4], base=16))
        battery_bits = battery_bits[len(battery_bits) - 4:]
        battery_bits = [battery_bits[i] for i in range(len(battery_bits) - 1,
                                                       -1, -1)]
        battery = sum([pow(i, 2) for i in range(len(battery_bits)) if
                       battery_bits[i] == '1'])

        return {
            'status': status,
            'vdd': battery
        }
