from uuid import UUID

import tedious.config
from bbbapi.controller.stockwerk_controller import StockwerkController

from bbbapi.controller.gebaeude_controller import GebaeudeController

from bbbapi.models.gebaeude import Gebaeude
from starlette.routing import Route
from tedious.asgi.starlette import ResourceController, StarletteApp
from tedious.res.auth_resource import AuthResource
from tedious.res.form_resource import FormResource
from tedious.sql.postgres import PostgreSQLDatabase

from bbbapi.controller.personal_controller import PersonalController
from bbbapi.models.personal import Personal
from bbbapi.models.stockwerk import Stockwerk

controller = None
auth_resource = None
personal_form_resource = None
gebaeude_form_resource = None
stockwerke_form_resource = None


async def login(request):
    """Route for login."""
    return await controller.handle(request, auth_resource)


async def personal_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Personal."""

    model = None
    if 'uuid' in request.path_params:
        model = Personal(uuid=UUID(hex=request.path_params['uuid']))
    return await controller.handle(request, personal_form_resource,
                                   model=model)


async def gebaeude_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Gebäuden."""

    model = None
    if 'id' in request.path_params:
        model = Gebaeude(_id=int(request.path_params['id']))
    return await controller.handle(request, gebaeude_form_resource, model=model)


async def stockwerk_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Stockwerken."""

    model = None
    if 'id' in request.path_params:
        model = Stockwerk(_id=int(request.path_params['id']))
    return await controller.handle(request, stockwerke_form_resource,
                                   model=model)

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

    global gebaeude_form_resource
    gebaeude_form_resource = FormResource(Gebaeude, GebaeudeController(), 'id')

    global stockwerke_form_resource
    stockwerke_form_resource = FormResource(Stockwerk, StockwerkController(), 'id')

    return StarletteApp(controller, [
        Route('/login', login, methods=["POST", "PUT", "DELETE"]),

        Route('/personal', personal_form, methods=["POST"]),
        Route('/personal/{uuid}', personal_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/gebaeude', gebaeude_form, methods=["POST"]),
        Route('/gebaeude/{id}', gebaeude_form, methods=["GET", "PUT", "DELETE"]),

        Route('/stockwerke', stockwerk_form, methods=["POST"]),
        Route('/stockwerke/{id}', stockwerk_form,
              methods=["GET", "PUT", "DELETE"]),
    ]).app
