import tedious.config
from bbbapi.routes import create_app
from .route_test_util import route_test
from ..util import get_admin_headers, get_personal_headers

tedious.config.load_config('config.ini')

app = create_app()

def test_gebaeude_route():

    route_test(app, get_admin_headers(), get_personal_headers(), {'name': 'Martinsberg'}, {'name': 'Bruggerstrasse'}, ['name'], 'id', '/gebaeude')