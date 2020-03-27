import tedious.config
from starlette.testclient import TestClient

from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_gebaeude, \
    create_stockwerk
import asyncio

tedious.config.load_config('config.ini')

app = create_app()


def test_stockwerke_route():
    gebaeude = asyncio.get_event_loop().run_until_complete(create_gebaeude())
    gebaeude2 = asyncio.get_event_loop().run_until_complete(create_gebaeude())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'name': 'Obergeschoss', 'niveau': 0, 'gebaeude': {'id': gebaeude["id"].value}},
               {'name': 'Obergeschoss', 'niveau': 0, 'gebaeude': {'id': gebaeude2["id"].value}},
               ['name', 'gebaeude.id'], 'id', '/stockwerke')


def test_stockwerke_list():
    # Falls es andere Daten in der Datenbank hat so ist dies unmöglich zum testen.
    app = create_app()

    for _ in range(3):
        asyncio.get_event_loop().run_until_complete(create_stockwerk())

    with TestClient(app) as client:
        response = client.get('/stockwerke', headers=get_admin_headers())
        assert response.status_code == 200