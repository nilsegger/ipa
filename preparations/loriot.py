"""Short sample implementation for connecting to LORIOT.
Websocket code is taken from https://websockets.readthedocs.io/en/stable/intro.html.
"""

import websockets
import asyncio
import ujson

from preparations.payload_decoders import lora_adeunis
from preparations.payload_decoders import elsys_ersoco2

token = "vgEAGQAAABZsb3JhLmF2ZWN0cmlzb25saW5lLmNoNkHslMchluLwH41kU_YDTg=="
uri = "wss://lora.avectrisonline.ch/app?token={}"

devices = {
    '0018B20000001CD0': lora_adeunis.decode,
    'A81758FFFE048CCA': elsys_ersoco2.decode,
}


async def serve():
    async with websockets.connect(uri.format(token)) as websocket:

        while True:
            message = await websocket.recv()
            json = ujson.decode(message)

            if json["cmd"] == "rx":
                # identifies type of message, rx = uplink message
                if "data" in json:
                    if json['EUI'] not in devices:
                        print("Please add device '{}' to devices.".format(json['EUI']))
                    else:
                        data = devices[json['EUI']](json['data'])
                        print("Device {} data:\n{}".format(json['EUI'], ujson.dumps(data, indent=2)))


asyncio.get_event_loop().run_until_complete(serve())
