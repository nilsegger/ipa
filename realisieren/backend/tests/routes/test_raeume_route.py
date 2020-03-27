import tedious.config
from starlette.testclient import TestClient

from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_stockwerk, create_raum
import asyncio

tedious.config.load_config('config.ini')

def test_raeume_route():
    app = create_app()
    stockwerk = asyncio.get_event_loop().run_until_complete(create_stockwerk())
    stockwerk2 = asyncio.get_event_loop().run_until_complete(create_stockwerk())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'name': '512', 'stockwerk': {'id': stockwerk["id"].value}},
               {'name': '502', 'stockwerk': {'id': stockwerk2["id"].value}},
               ['name', 'stockwerk.id'], 'id', '/raeume')


def test_raeume_list():
    # Falls es andere Daten in der Datenbank hat so ist dies unmöglich zum testen.
    app = create_app()

    for _ in range(3):
        asyncio.get_event_loop().run_until_complete(create_raum())

    with TestClient(app) as client:
        response = client.get('/raeume', headers=get_admin_headers())
        assert response.status_code == 200