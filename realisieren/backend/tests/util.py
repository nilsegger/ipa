from tedious.util import create_uuid

from bbbapi.controller.personal_controller import PersonalController
from bbbapi.controller.stockwerk_controller import StockwerkController
from bbbapi.models.personal import Personal

from bbbapi.models.stockwerk import Stockwerk

from bbbapi.controller.gebaeude_controller import GebaeudeController

from bbbapi.models.gebaeude import Gebaeude
from tedious.auth.auth import Auth
from tedious.tests.util import TestConnection

from bbbapi.common_types import Roles
import asyncio
import tedious.config


def create_admin_access_token():
    """Erstellt einen Access Token für den Admin Benutzer mit der UUID 8a733d6a-80d0-41c9-a2a8-b6302da731c9"""
    return asyncio.get_event_loop().run_until_complete(Auth().create_token(
        audience=tedious.config.CONFIG["TOKEN"]["audience"],
        claims={'uid': '6a3d738ad080c941a2a8b6302da731c9',
                'name': 'Admin',
                'role': Roles.ADMIN.value}))


def create_non_admin_token():
    """Erstellt einen Access Token für ein Personal Mitarbeiter."""
    return asyncio.get_event_loop().run_until_complete(Auth().create_token(
        audience=tedious.config.CONFIG["TOKEN"]["audience"],
        claims={'uid': '6a3d738ad080caaaaaaab6302da731c9',
                'name': 'Personal',
                'role': Roles.PERSONAL.value}))


def get_admin_headers():
    """Erstellt den Authorization Header welcher dafür benützt wird einen Authorisierten Aufruf auf die Datenbank zu machen."""
    return {'Authorization': 'Bearer {}'.format(
        create_admin_access_token().decode('utf-8'))}


def get_personal_headers():
    """Erstellt den Authorization Header welcher dafür benützt wird einen Authorisierten Aufruf auf die Datenbank zu machen."""
    return {'Authorization': 'Bearer {}'.format(
        create_non_admin_token().decode('utf-8'))}


async def create_personal():
    async with TestConnection() as connection:
        model = Personal()
        model["benutzername"].value = create_uuid().hex[:30]
        model["rolle"].value = Roles.PERSONAL
        model["name"].value = "Test Benutzer"
        model["passwort"].value = "123456"
        await PersonalController().create(connection, model)
        return model

async def create_gebaeude():
    model = Gebaeude()
    model["name"].value = "Test Gebäude"
    async with TestConnection() as connection:
        await GebaeudeController().create(connection, model)
    return model


async def create_stockwerk():
    gebaeude = await create_gebaeude()
    model = Stockwerk()
    model["name"].value = "Test Stockwerk"
    model["niveau"].value = 0
    model["gebaeude"]["id"].value = gebaeude["id"].value
    async with TestConnection() as connection:
        await StockwerkController().create(connection, model)
    return model
