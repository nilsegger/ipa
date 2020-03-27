import tedious.config
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers, create_gebaeude
import asyncio

tedious.config.load_config('config.ini')

app = create_app()


def test_stockwerke_route():
    gebaeude = asyncio.get_event_loop().run_until_complete(create_gebaeude())
    gebaeude2 = asyncio.get_event_loop().run_until_complete(create_gebaeude())

    route_test(app, get_admin_headers(), get_personal_headers(),
               {'name': 'Obergeschoss', 'niveau': 0, 'gebaeude': {'id': gebaeude["id"].value}},
               {'name': 'Obergeschoss', 'niveau': 0, 'gebaeude': {'id': gebaeude2["id"].value}},
               ['name', 'gebaeude.id'], 'id', '/stockwerke')
