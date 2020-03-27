import tedious.config
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
        auth = Auth()
        await auth.register(connection, 'admin', 'test', Roles.ADMIN.value)

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(setup_admin())
