import tedious.config

from bbbapi.common_types import BeobachterArt
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_raum, \
    create_sensor
import asyncio

tedious.config.load_config('config.ini')


def test_beobachter_route():
    app = create_app()

    sensor = asyncio.get_event_loop().run_until_complete(create_sensor())
    sensor2 = asyncio.get_event_loop().run_until_complete(create_sensor())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'sensor': {'dev_eui': sensor["dev_eui"].value}, 'name': 'Temperatur Beobachter', 'wertName': 'temperur', 'ausloeserWert': 18, 'art': BeobachterArt.RICHTWERT_DARUNTER.value},
               {'sensor': {'dev_eui': sensor2["dev_eui"].value}, 'name': 'Temperatur Beobachter Update', 'wertName': 'temperatur', 'ausloeserWert': 26, 'art': BeobachterArt.RICHTWERT_DARUEBER.value},
               ['sensor.dev_eui', 'name', 'wertName', 'ausloeserWert', 'art'], 'id', '/beobachter')
