"""Short sample implementation for connecting to LORIOT.
Websocket code is taken from https://websockets.readthedocs.io/en/stable/intro.html.
This implementation parses the data according to https://www.adeunis.com/wp-content/uploads/2017/08/User_Guide_FTD_LoRaWAN_EU863-870_V1.2.3.pdf page 42.
"""

import websockets
import asyncio
import ujson

token = "vgEAGQAAABZsb3JhLmF2ZWN0cmlzb25saW5lLmNoNkHslMchluLwH41kU_YDTg=="
uri = "wss://lora.avectrisonline.ch/app?token={}"


async def decode_payload(payload):
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

    print("-------------------------------------------------------")
    print("Temperature present", temperature_present)
    print("Triggered by accelerometer", triggered_by_accelerometer)
    print("Triggered by button", triggered_by_button)
    print("GPS present", gps_present)
    print("Uplink counter present", uplink_counter_present)
    print("Downlink counter present", downlink_counter_present)
    print("Battery level present", downlink_counter_present)
    print("Battery level present", battery_level_present)
    print("RSSI and SNR present level present", rssi_snr_present)

    if temperature_present:
        temperature_bits = bin(payload[1])[2:]
        temperature = sum([pow(2, len(temperature_bits) - 1 - i) for i in range(len(temperature_bits)) if temperature_bits[i] == '1'])
        print("Temperature {}".format(temperature))

    print("-------------------------------------------------------")


async def serve():
    async with websockets.connect(uri.format(token)) as websocket:

        while True:
            message = await websocket.recv()
            json = ujson.decode(message)

            if json["cmd"] == "rx":
                # identifies type of message, rx = uplink message
                if "data" in json:
                    payload = bytearray.fromhex(json["data"])
                    await decode_payload(payload)


asyncio.get_event_loop().run_until_complete(serve())
