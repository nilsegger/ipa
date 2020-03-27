import asyncio

import tedious.config
from starlette.testclient import TestClient

from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_gebaeude

tedious.config.load_config('config.ini')



def test_gebaeude_route():
    app = create_app()
    route_test(app, get_admin_headers(), get_personal_headers(), {'name': 'Martinsberg'}, {'name': 'Bruggerstrasse'}, ['name'], 'id', '/gebaeude')

def test_gebaeude_list():
    # Falls es andere Daten in der Datenbank hat so ist dies unmöglich zum testen.
    app = create_app()

    for _ in range(3):
        asyncio.get_event_loop().run_until_complete(create_gebaeude())

    with TestClient(app) as client:
        response = client.get('/gebaeude', headers=get_admin_headers())
        assert response.status_code == 200