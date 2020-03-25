import tedious.config
from tedious.asgi.starlette import ResourceController, StarletteApp
from tedious.res.auth_resource import AuthResource
from tedious.sql.postgres import PostgreSQLDatabase
from starlette.routing import Route

tedious.config.load_config('config.ini')

controller = ResourceController(
    PostgreSQLDatabase(**tedious.config.CONFIG["DB_CREDENTIALS"]))

auth = AuthResource()


async def login(request):
    return await controller.handle(request, auth)


app = StarletteApp(controller, [
    Route('/login', login, methods=["POST", "PUT", "DELETE"])
]).app
