import tedious.config
from bbbapi.models.personal import Personal

from bbbapi.controller.personal_controller import PersonalController
from tedious.auth.auth import Auth
from tedious.tests.util import TestConnection

from bbbapi.common_types import Roles
from bbbapi.routes import create_app

"""
    Loads configuration from config.ini file.
"""
tedious.config.load_config('config.ini')

"""
    create_app returns the actual servable app and adds all routes to it.
"""
app = create_app()


async def setup_admin():
    async with TestConnection() as connection:
        model = Personal()
        model['name'].value = 'Administrator'
        model['benutzername'].value = 'admin'
        model['passwort'].value = '12345678'
        model['rolle'].value = Roles.ADMIN
        await PersonalController().create(connection, model)

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(setup_admin())
