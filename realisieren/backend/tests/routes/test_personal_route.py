from starlette.testclient import TestClient
import tedious.config
from bbbapi.common_types import Roles
from bbbapi.routes import create_app
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


def test_routes():
    headers = get_admin_headers()
    create_request = {
        'name': 'Hello World!',
        'benutzername': 'reinigung@bbbaden.ch',
        'passwort': '123456',
        'rolle': Roles.PERSONAL.value
    }
    update_request = {
        'name': 'Hello BBB!',
        'benutzername': 'admin@bbbaden.ch',
        'passwort': '654321',
        'rolle': Roles.ADMIN.value
    }

    with TestClient(app) as client:
        # Create Model
        response = client.post('/personal', headers=headers,
                               json=create_request)
        assert response.status_code == 200, "Response: {}".format(
            response.text)
        json = response.json()
        assert 'uuid' in json

        uri = '/personal/{}'.format(json['uuid'])

        # Verify data
        compare_global(client, uri, headers, create_request)

        # Update Model
        response = client.put(uri, headers=headers, json=update_request)
        assert response.status_code == 200

        # Verify data
        compare_global(client, uri, headers, update_request)

        # Nicht authorisierter Zugriff
        response = client.put(uri, headers=get_personal_headers(), json=update_request)
        assert response.status_code == 403

        # Delete Model
        response = client.delete(uri, headers=headers)
        assert response.status_code == 200

        # Prüfen das Model auch wirklich gelöscht wurde
        response = client.get(uri, headers=headers)
        assert response.status_code == 404


