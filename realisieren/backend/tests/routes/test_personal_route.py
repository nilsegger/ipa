import tedious.config
from starlette.testclient import TestClient
import asyncio
from bbbapi.common_types import Roles
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_personal

tedious.config.load_config('config.ini')



def test_personal_form():
    app = create_app()
    route_test(app, get_admin_headers(), get_personal_headers(),
               {
                   'name': 'Hello World!',
                   'benutzername': 'reinigung@bbbaden.ch',
                   'passwort': '123456',
                   'rolle': Roles.PERSONAL.value
               }, {
                   'name': 'Hello BBB!',
                   'benutzername': 'admin@bbbaden.ch',
                   'passwort': '654321',
                   'rolle': Roles.ADMIN.value
               }, ['name', 'benutzername', 'rolle'],
               'uuid', '/personal')


def test_personal_list():
    app = create_app()
    personal = [asyncio.get_event_loop().run_until_complete(create_personal()) for _ in range(5)]

    with TestClient(app) as client:
        response = client.get('/personal', headers=get_admin_headers())
        assert response.status_code == 200