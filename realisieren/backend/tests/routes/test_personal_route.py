from starlette.testclient import TestClient
import tedious.config
from bbbapi.common_types import Roles
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers

tedious.config.load_config('config.ini')

app = create_app()


def compare_global(client, uri, headers, expected):
    response = client.get(uri, headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json['name'] == expected['name']
    assert json['benutzername'] == expected['benutzername']
    assert json['rolle'] == expected['rolle']


def test_personal_route():
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