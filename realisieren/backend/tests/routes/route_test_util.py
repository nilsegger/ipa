from starlette.testclient import TestClient
from tedious.util import KeyPathsIter


def compare_dict(fields, actual, expected):
    if isinstance(fields, list):
        fields = KeyPathsIter(fields)

    for key, _iter in fields:
        if _iter is None:
            assert actual[key] == expected[key]
        else:
            compare_dict(_iter, actual[key], expected[key])


def compare_global(fields, client, uri, headers, expected):
    response = client.get(uri, headers=headers)
    assert response.status_code == 200
    json = response.json()
    compare_dict(fields, json, expected)


def route_test(app, valid_header, invalid_header, create_request,
               update_request,
               compare_fields, identifier, uri):
    """Testet Route ob Modell erstellt, aktualisiert und gelöscht werden kann.
    Testet zusätzlich unatuorisierter Zugriff und Zugriff auf nicht existierendes Modell.

    Args:
        valid_header: Dict mit einem validen Authorization header
        invalid_header: Dict mit einem invaliden Authorization header
        create_request: Dict mit allen Werten für das Erstellen eines Modells.
        update_request: Dict mit allen Werten für das Aktualisieren eines Modells.
        compare_fields: Felder welche schlussendlich beim Vergleich zwischen dem Datenbank Modell und lokalen Modell verglichen werden.
        identifier: Key welcher aus dem POST Request entzogen werden soll und an die URI angehängt werden soll.
        uri: URI welche zur Resource zeigt,
    """

    with TestClient(app) as client:
        # Create Model
        response = client.post(uri, headers=valid_header,
                               json=create_request)
        assert response.status_code == 200, response.content
        json = response.json()
        assert identifier in json

        uri = '{}/{}'.format(uri, json[identifier])

        # Verify data
        compare_global(compare_fields, client, uri, valid_header,
                       create_request)

        # Update Model
        response = client.put(uri, headers=valid_header, json=update_request)
        assert response.status_code == 200

        # Verify data
        compare_global(compare_fields, client, uri, valid_header,
                       update_request)

        # Nicht authorisierter Zugriff
        response = client.put(uri, headers=invalid_header, json=update_request)
        assert response.status_code == 403

        # Delete Model
        response = client.delete(uri, headers=valid_header)
        assert response.status_code == 200

        # Prüfen das Model auch wirklich gelöscht wurde
        response = client.get(uri, headers=valid_header)
        assert response.status_code == 404
