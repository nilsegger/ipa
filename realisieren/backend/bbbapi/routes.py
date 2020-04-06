from uuid import UUID

import tedious.config
from bbbapi.controller.beobachter_list_controller import \
    BeobachterListController
from bbbapi.controller.materialien_list_controller import \
    MaterialienListController
from tedious.res.list_resource import StaticListResource

from bbbapi.common_types import Roles
from bbbapi.controller.beobachter_controller import BeobachterController
from bbbapi.controller.gebaeude_list_controller import GebaeudeListController
from bbbapi.controller.material_controller import MaterialController
from bbbapi.controller.personal_list_controller import PersonalListController
from bbbapi.controller.raeume_list_controller import RaeumeListController
from bbbapi.controller.raum_controller import RaumController
from bbbapi.controller.sensor_controller import SensorController
from bbbapi.controller.sensoren_list_controller import SensorenListController
from bbbapi.controller.stockwerke_list_controller import \
    StockwerkeListController
from bbbapi.models.beobachter import Beobachter
from bbbapi.models.material import Material
from bbbapi.models.meldung import Meldung

from bbbapi.models.raum import Raum

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
from bbbapi.models.sensor import Sensor
from bbbapi.models.stockwerk import Stockwerk
from bbbapi.resources.beobachter_zu_materialien_list_resource import \
    MaterialienZuBeobachterListResource
from bbbapi.resources.meldung_form_resource import MeldungFormResource
from bbbapi.resources.meldungen_list_resource import MeldungenListResource
from bbbapi.resources.material_zu_beobachter_resource import MaterialZuBeobachterResource
from bbbapi.resources.sensor_beobachter_list_resource import \
    SensorBeobachterListResource
from bbbapi.resources.sensor_wert_list_resource import SensorWertListResource

controller = None
auth_resource = None
personal_form_resource = None
personal_list_resource = None
gebaeude_form_resource = None
gebaeude_list_resource = None
stockwerke_form_resource = None
stockwerke_list_resource = None
raeume_form_resource = None
raeume_list_resource = None
sensor_form_resource = None
sensoren_list_resource = None
meldungen_form_resource = None
meldungen_list_resource = None
beobachter_form_resource = None
beobachter_list_resource = None
materialien_form_resource = None
material_list_resource = None
material_zu_beobachter_resource = None

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


async def personal_list(request):
    """Auflistung des Personal."""
    return await controller.handle(request, personal_list_resource)


async def gebaeude_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Gebäuden."""

    model = None
    if 'id' in request.path_params:
        model = Gebaeude(_id=int(request.path_params['id']))
    return await controller.handle(request, gebaeude_form_resource,
                                   model=model)


async def gebaeude_list(request):
    """Auflistung aller Gebäude."""
    return await controller.handle(request, gebaeude_list_resource)


async def stockwerk_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Stockwerken."""

    model = None
    if 'id' in request.path_params:
        model = Stockwerk(_id=int(request.path_params['id']))
    return await controller.handle(request, stockwerke_form_resource,
                                   model=model)


async def stockwerke_list(request):
    """Auflistung aller Stockwerke."""
    return await controller.handle(request, stockwerke_list_resource)


async def raeume_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Räume."""

    model = None
    if 'id' in request.path_params:
        model = Raum(_id=int(request.path_params['id']))
    return await controller.handle(request, raeume_form_resource, model=model)


async def raeume_list(request):
    """Auflistung aller Räume."""
    return await controller.handle(request, raeume_list_resource)


async def sensor_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Sensoren."""

    model = None
    if 'dev_eui' in request.path_params:
        model = Sensor(dev_eui=request.path_params['dev_eui'])
    return await controller.handle(request, sensor_form_resource, model=model)


async def sensoren_list(request):
    """Auflistung aller Sensoren."""
    return await controller.handle(request, sensoren_list_resource)


async def meldungen_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Meldungen."""

    model = None
    if 'id' in request.path_params:
        model = Meldung(_id=int(request.path_params['id']))
    return await controller.handle(request, meldungen_form_resource,
                                   model=model)


async def meldungen_list(request):
    """Auflistungen der Meldungen."""
    return await controller.handle(request, meldungen_list_resource)


async def beobachter_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Beobachtern."""

    model = None
    if 'id' in request.path_params:
        model = Beobachter(_id=int(request.path_params['id']))
    return await controller.handle(request, beobachter_form_resource,
                                   model=model)


async def beobachter_list(request):
    """Auflistungen der Beobachter."""
    return await controller.handle(request, beobachter_list_resource)


async def materialien_form(request):
    """Route für das Erstellen, Aktualisieren und Löschen von Beobachtern."""

    model = None
    if 'id' in request.path_params:
        model = Material(_id=int(request.path_params['id']))
    return await controller.handle(request, materialien_form_resource,
                                   model=model)


async def materialien_list(request):
    """Auflistungen der Materialien."""
    return await controller.handle(request, material_list_resource)


async def material_zu_beobachter_form(request):
    """Route für das Hinzufügen oder Löschen von Material zu Beobachtern."""

    if 'id' in request.path_params and 'mid' in request.path_params:
        beobachter = Beobachter(_id=int(request.path_params['id']))
        material = Material(_id=int(request.path_params['mid']))
        return await controller.handle(request,
                                       material_zu_beobachter_resource,
                                       beobachter=beobachter, material=material)
    else:
        return await controller.handle(request,
                                       material_zu_beobachter_resource,
                                       material_zu_beobachter_id=
                                       int(request.path_params['id']))


async def material_zu_beobachter_list(request):
    """Erstellt eine Auflistung von allen Materialien für einen Beobachter."""

    beobachter = Beobachter(_id=int(request.path_params['id']))
    return await controller.handle(request,
                                   MaterialienZuBeobachterListResource(
                                       beobachter))


async def sensor_beobachter_list(request):
    """Erstellt eine Auflistung von allen Beobachtern eines Sensors."""
    sensor = Sensor(dev_eui=request.path_params['dev_eui'])
    return await controller.handle(request, SensorBeobachterListResource(sensor))


async def sensor_wert_list(request):
    """Erstellt eine Auflistung von allen Werten eines Sensors."""
    sensor = Sensor(dev_eui=request.path_params['dev_eui'])
    return await controller.handle(request, SensorWertListResource(sensor))


def create_app():
    """Creates app and adds all routes."""
    global controller

    if controller is None:
        # Values have not yet been set.

        controller = ResourceController(
            PostgreSQLDatabase(**tedious.config.CONFIG["DB_CREDENTIALS"]))

        global auth_resource
        auth_resource = AuthResource()

        global personal_form_resource
        personal_form_resource = FormResource(Personal, PersonalController(),
                                              'uuid')

        global personal_list_resource
        personal_list_resource = StaticListResource(PersonalListController(),
                                                    [Roles.ADMIN.value],
                                                    ['uuid', 'name',
                                                     'benutzername', 'rolle'],
                                                    join_foreign_keys=True)

        global gebaeude_form_resource
        gebaeude_form_resource = FormResource(Gebaeude, GebaeudeController(),
                                              'id')

        global gebaeude_list_resource
        gebaeude_list_resource = StaticListResource(GebaeudeListController(),
                                                    [Roles.ADMIN.value,
                                                     Roles.PERSONAL.value],
                                                    ['id', 'name'])

        global stockwerke_form_resource
        stockwerke_form_resource = FormResource(Stockwerk,
                                                StockwerkController(),
                                                'id')

        global stockwerke_list_resource
        stockwerke_list_resource = StaticListResource(
            StockwerkeListController(),
            [Roles.ADMIN.value,
             Roles.PERSONAL.value],
            ['id', 'name', 'niveau', 'gebaeude.id', 'gebaeude.name'],
            join_foreign_keys=True)

        global raeume_form_resource
        raeume_form_resource = FormResource(Raum, RaumController(), 'id')

        global raeume_list_resource
        raeume_list_resource = StaticListResource(
            RaeumeListController(),
            [Roles.ADMIN.value,
             Roles.PERSONAL.value],
            ['id', 'name', 'stockwerk.id', 'stockwerk.name',
             'stockwerk.niveau', 'gebaeude.id', 'gebaeude.name'],
            join_foreign_keys=True)

        global sensor_form_resource
        sensor_form_resource = FormResource(Sensor, SensorController(),
                                            'dev_eui')

        global sensoren_list_resource
        sensoren_list_resource = StaticListResource(SensorenListController(),
                                                    [Roles.ADMIN.value,
                                                     Roles.PERSONAL.value],
                                                    ['dev_eui', 'name', 'art',
                                                     'raum.id', 'raum.name',
                                                     'stockwerk.id',
                                                     'stockwerk.name',
                                                     'stockwerk.niveau',
                                                     'gebaeude.id',
                                                     'gebaeude.name'],
                                                    join_foreign_keys=True)

    global meldungen_form_resource
    meldungen_form_resource = MeldungFormResource()

    global meldungen_list_resource
    meldungen_list_resource = MeldungenListResource(limit=25)

    global beobachter_form_resource
    beobachter_form_resource = FormResource(Beobachter, BeobachterController(),
                                            'id')

    global beobachter_list_resource
    beobachter_list_resource = StaticListResource(BeobachterListController(), [Roles.ADMIN.value,
                                                 Roles.PERSONAL.value], ['id', 'name', 'art', 'stand', 'ausloeserWert', 'wertName', 'sensor.dev_eui', 'sensor.name'], join_foreign_keys=True)


    global materialien_form_resource
    materialien_form_resource = FormResource(Material, MaterialController(),
                                             'id')

    global material_list_resource
    material_list_resource = StaticListResource(MaterialienListController(),
                                                [Roles.ADMIN.value,
                                                 Roles.PERSONAL.value],
                                                ['id', 'name'])

    global material_zu_beobachter_resource
    material_zu_beobachter_resource = MaterialZuBeobachterResource()

    return StarletteApp(controller, [
        Route('/login', login, methods=["POST", "PUT", "DELETE"]),

        Route('/personal', personal_list, methods=["GET"]),
        Route('/personal', personal_form, methods=["POST"]),
        Route('/personal/{uuid}', personal_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/gebaeude', gebaeude_list, methods=["GET"]),
        Route('/gebaeude', gebaeude_form, methods=["POST"]),
        Route('/gebaeude/{id}', gebaeude_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/stockwerke', stockwerke_list, methods=["GET"]),
        Route('/stockwerke', stockwerk_form, methods=["POST"]),
        Route('/stockwerke/{id}', stockwerk_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/raeume', raeume_list, methods=["GET"]),
        Route('/raeume', raeume_form, methods=["POST"]),
        Route('/raeume/{id}', raeume_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/sensoren', sensoren_list, methods=["GET"]),
        Route('/sensoren', sensor_form, methods=["POST"]),
        Route('/sensoren/{dev_eui}', sensor_form,
              methods=["GET", "PUT", "DELETE"]),
        Route('/sensoren/{dev_eui}/beobachter', sensor_beobachter_list, methods=["GET", "PUT", "DELETE"]),
        Route('/sensoren/{dev_eui}/werte', sensor_wert_list, methods=["GET", "PUT", "DELETE"]),

        Route('/meldungen', meldungen_list, methods=["GET"]),
        Route('/meldungen', meldungen_form, methods=["POST"]),
        Route('/meldungen/{id}', meldungen_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/beobachter', beobachter_list, methods=["GET"]),
        Route('/beobachter', beobachter_form, methods=["POST"]),
        Route('/beobachter/{id}', beobachter_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/beobachter/{id}/materialien', material_zu_beobachter_list,
              methods=["GET"]),

        Route('/materialien', materialien_list, methods=["GET"]),
        Route('/materialien', materialien_form, methods=["POST"]),
        Route('/materialien/{id}', materialien_form,
              methods=["GET", "PUT", "DELETE"]),

        Route('/beobachter/{id}/materialien/{mid}',
              material_zu_beobachter_form, methods=['POST']),
        Route('/beobachter/materialien/{id}', material_zu_beobachter_form,
              methods=['DELETE'])
    ]).app
