import tedious.config
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_raum, \
    create_sensor
import asyncio

tedious.config.load_config('config.ini')


def test_meldungen_route():
    app = create_app()
    sensor = asyncio.get_event_loop().run_until_complete(create_sensor())
    sensor2 = asyncio.get_event_loop().run_until_complete(create_sensor())

    route_test(app, get_admin_headers(), {},
               {'sensor': {'dev_eui': sensor["dev_eui"].value}, 'beschreibung': 'Sensor Kaputt!',
                'raum': {'id': sensor["raum"]["id"].value}},
               {'sensor': {'dev_eui': sensor2["dev_eui"].value},
                'beschreibung': 'WC spühlung kaputt.',
                'raum': {'id': sensor2["raum"]["id"].value}},
               ['sensor.dev_eui', 'raum.id', 'beschreibung'], 'id', '/meldungen')
