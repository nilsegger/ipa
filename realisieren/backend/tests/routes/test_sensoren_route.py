import tedious.config
from starlette.testclient import TestClient
import random
from bbbapi.common_types import SensorTypes
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_raum, create_sensor
import asyncio

tedious.config.load_config('config.ini')

def test_sensoren_route():
    app = create_app()
    raum = asyncio.get_event_loop().run_until_complete(create_raum())
    raum2 = asyncio.get_event_loop().run_until_complete(create_raum())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'dev_eui': ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(16)), 'name': 'Sensor 1', 'art': SensorTypes.ADEUNIS_RF.value, 'raum': {'id': raum["id"].value}},
               {'name': 'Sensor 1.0', 'art': SensorTypes.ELSYS_ERS_CO2.value, 'raum': {'id': raum2["id"].value}},
               ['name', 'art', 'raum.id'], 'dev_eui', '/sensoren')


def test_sensoren_list():
    # Falls es andere Daten in der Datenbank hat so ist dies unmöglich zum testen.
    app = create_app()

    for _ in range(3):
        asyncio.get_event_loop().run_until_complete(create_sensor())

    with TestClient(app) as client:
        response = client.get('/sensoren', headers=get_admin_headers())
        assert response.status_code == 200
