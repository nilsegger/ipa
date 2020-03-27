import tedious.config
from starlette.routing import Route
from tedious.asgi.starlette import ResourceController, StarletteApp
from tedious.res.auth_resource import AuthResource
from tedious.res.form_resource import FormResource
from tedious.sql.postgres import PostgreSQLDatabase

from bbbapi.controller.personal_controller import PersonalController
from bbbapi.models.personal import Personal

controller = None
auth_resource = None
personal_form_resource = None


async def login(request):
    """Route for login."""
    return await controller.handle(request, auth_resource)


async def personal_form(request):
    """Route für das Erstellen und Löschen von Personal."""
    print("Hello??")
    return await controller.handle(request, personal_form_resource)


def create_app():
    """Creates app and adds all routes."""
    global controller
    controller = ResourceController(
        PostgreSQLDatabase(**tedious.config.CONFIG["DB_CREDENTIALS"]))

    global auth_resource
    auth_resource = AuthResource()

    global personal_form_resource
    personal_form_resource = FormResource(Personal, PersonalController(),
                                          'uuid')

    return StarletteApp(controller, [
        Route('/login', login, methods=["POST", "PUT", "DELETE"]),
        Route('/personal', personal_form, methods=["POST"])
    ]).app
