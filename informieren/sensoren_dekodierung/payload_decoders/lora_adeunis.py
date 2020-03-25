"""
    Sample LoRa Alliance Adeunis payloader decoder.

    This implementation parses the data according to https://www.adeunis.com/wp-content/uploads/2017/08/User_Guide_FTD_LoRaWAN_EU863-870_V1.2.3.pdf page 42.
"""


def decode(payload):
    payload = bytearray.fromhex(payload)

    status = bin(payload[0])[2:]  # [2:] removes 0b python binary prefix.

    if len(status) < 8:
        status = ''.join(['0' for _ in range(8 - len(status))]) + status

    """
    Bit N° / Comment Value
    7 / Presence of temperature information / 0 or 1
    6 / Transmission triggered by the accelerometer / 0 or 1
    5 / Transmission triggered by pressing pushbutton / 1 0 or 1
    4 / Presence of GPS information / 0 or 1
    3 / Presence of Uplink frame counter / 0 or 1
    2 / Presence of Downlink frame counter / 0 or 1
    1 / Presence of battery level information / 0 or 1
    1 / Presence of RSSI and SNR information / 0 or 1

    0: Data missing from the payload
    1: Data present in the payload
    """

    temperature_present = status[0] == '1'
    triggered_by_accelerometer = status[1] == '1'
    triggered_by_button = status[2] == '1'
    gps_present = status[3] == '1'
    uplink_counter_present = status[4] == '1'
    downlink_counter_present = status[5] == '1'
    battery_level_present = status[6] == '1'
    rssi_snr_present = status[7] == '1'

    result = {}

    if temperature_present:
        temperature_bits = bin(payload[1])[2:]
        temperature = sum([pow(2, len(temperature_bits) - 1 - i) for i in range(len(temperature_bits)) if temperature_bits[i] == '1'])
        result['temperature'] = temperature
    return result
