from typing import Dict, Any
from decoders.decoder import Decoder


class ElsysDecoder(Decoder):
    """Implementation für die Dekodierung eines Wertes eines Elsys ERS CO2
    Sensors. Basierend auf das `Datenblatt <https://elsys.se/public/datasheets/ERS_CO2_datasheet.pdf>`__.
    """

    async def decode(self, data: str) -> Dict[str, Any]:
        """Dekodiert data in die Werte
            - Temperatur
            - Feuchtigkeit
            - Licht
            - Bewegung
            - CO2
            - Batterie Spannung

        Args:
            data (str): Elsys ERS CO2 Sensor Wert im Hex Format.

        Returns:
            Ein Dict, welches die Oben genannten Werte enthält.
        """

        # Der untenstehende Code ist als Vorarbeit deklariert.

        decoded = {}

        i = 0
        while i < len(data):

            _type = int(data[i:i + 2], base=16)
            i += 2

            if _type == 0x01:  # Temperature
                # (Value of: 100 -> 10.0 °C)
                _bytes = data[i:i + 4]
                i += 4
                decoded['temperature'] = int(_bytes, base=16) / 10
            elif _type == 0x02:  # Humidity
                _bytes = data[i:i + 2]
                i += 2
                decoded['humidity'] = int(_bytes, base=16)
            elif _type == 0x04:  # Light
                _bytes = data[i:i + 4]
                i += 4
                decoded['light'] = int(_bytes, base=16)
            elif _type == 0x05:  # Motion PIR
                _bytes = data[i:i + 2]
                i += 2
                decoded['motion'] = int(_bytes, base=16)
            elif _type == 0x06:  # CO2
                _bytes = data[i:i + 4]
                i += 4
                decoded['co2'] = int(_bytes, base=16)
            elif _type == 0x07:  # Battery voltage 0 – 65535 mV
                _bytes = data[i:i + 4]
                i += 4
                decoded['vdd'] = int(_bytes, base=16)

        return decoded
