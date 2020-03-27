from tedious.auth.auth import Auth
from bbbapi.common_types import Roles
import asyncio
import tedious.config


def create_admin_access_token():
    """Erstellt einen Access Token für den Admin Benutzer mit der UUID 8a733d6a-80d0-41c9-a2a8-b6302da731c9"""
    return asyncio.get_event_loop().run_until_complete(Auth().create_token(
        audience=tedious.config.CONFIG["TOKEN"]["audience"],
        claims={'uid': '6a3d738ad080c941a2a8b6302da731c9',
                'name': 'Admin',
                'role': Roles.ADMIN.value}))


def get_admin_headers():
    """Erstellt den Authorization Header welcher dafür benützt wird einen Authorisierten Aufruf auf die Datenbank zu machen."""
    return {'Authorization': 'Bearer {}'.format(create_admin_access_token().decode('utf-8'))}
