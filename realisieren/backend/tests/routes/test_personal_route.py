from starlette.testclient import TestClient
import tedious.config
from bbbapi.common_types import Roles
from bbbapi.routes import create_app
from ..util import get_admin_headers

tedious.config.load_config('config.ini')

app = create_app()


def test_create():
    headers = get_admin_headers()
    request_json = {
        'name': 'Hello World!',
        'benutzername': 'reinigung@bbbaden.ch',
        'passwort': '123456',
        'rolle': Roles.PERSONAL.value
    }

    with TestClient(app) as client:
        client = TestClient(app)

        response = client.post('/personal', headers=headers, json=request_json)

        assert response.status_code == 200, "Response: {}".format(response.text)
