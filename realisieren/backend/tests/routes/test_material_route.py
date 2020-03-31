import tedious.config
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers

tedious.config.load_config('config.ini')

app = create_app()


def test_materialien_route():

    route_test(app, get_admin_headers(), {},
               {'name': 'WC-Papier'},
               {'name': 'Seife'},
               ['name'], 'id', '/materialien')
