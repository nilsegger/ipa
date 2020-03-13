"""
    Sample Elsys ERSOCO2 payload decoder.

    sample data: 01 00 f1 02 1d 04 00 c0 05 00 06 02 4a 07 0e 40

    expected:
        {
            "temperature": 24.1,
            "humidity": 29,
            "light": 192,
            "motion": 0,
            "co2": 586,
            "vdd": 3648
        }

    https://elsys.se/public/documents/Elsys-LoRa-payload.pdf
    https://elsys.se/public/datasheets/ERS_CO2_datasheet.pdf

    Type value Type Data size Comment
    0x01 Temperature 2 -3276.5 °C → 3276.5 °C (Value of: 100 → 10.0 °C)
    0x02 Humidity 1 0 – 100 %
    0x04 Light 2 0 – 65535 Lux
    0x05 Motion (PIR) 1 0 – 255 (Number of motion counts)
    0x06 CO2 2 0 – 10000 ppm
    0x07 VDD (Battery voltage) 2 0 – 65535 mV
    0x3D Debug information 4 Data depends on debug information
    0x3E Sensor settings n Sensor setting sent to server at startup (first package). Sent on Port+1.
"""


def decode(payload):
    decoded = {}

    i = 0
    while i < len(payload):

        _type = int(payload[i:i + 2], base=16)
        i += 2

        if _type == 0x01:  # Temperature
            # (Value of: 100 -> 10.0 °C)
            _bytes = payload[i:i + 4]
            i += 4
            decoded['temperature'] = int(_bytes, base=16) / 10
        elif _type == 0x02:  # Humidity
            _bytes = payload[i:i + 2]
            i += 2
            decoded['humidity'] = int(_bytes, base=16)
        elif _type == 0x04:  # Light
            _bytes = payload[i:i + 4]
            i += 4
            decoded['light'] = int(_bytes, base=16)
        elif _type == 0x05:  # Motion PIR
            _bytes = payload[i:i + 2]
            i += 2
            decoded['motion'] = int(_bytes, base=16)
        elif _type == 0x06:  # CO2
            _bytes = payload[i:i + 4]
            i += 4
            decoded['co2'] = int(_bytes, base=16)
        elif _type == 0x07:  # Battery voltage 0 – 65535 mV
            _bytes = payload[i:i + 4]
            i += 4
            decoded['vdd'] = int(_bytes, base=16)

    return decoded


if __name__ == '__main__':
    print(decode('0100f1021d0400c0050006024a070e40'))
