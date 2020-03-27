import tedious.config
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_stockwerk
import asyncio

tedious.config.load_config('config.ini')

app = create_app()


def test_raeume_route():
    stockwerk = asyncio.get_event_loop().run_until_complete(create_stockwerk())
    stockwerk2 = asyncio.get_event_loop().run_until_complete(create_stockwerk())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'name': '512', 'stockwerk': {'id': stockwerk["id"].value}},
               {'name': '502', 'stockwerk': {'id': stockwerk2["id"].value}},
               ['name', 'stockwerk.id'], 'id', '/raeume')
