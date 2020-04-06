from typing import Dict, Tuple, Any, List

from bbbapi.controller.raum_controller import RaumController

from bbbapi.util import sanitize_fields
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.common_types import Roles


class SensorController(ModelController):
    """Controller für die Erstelltung, Aktualisierung und Löschung von Sensoren."""

    def __init__(self):
        super().__init__('Sensoren', 'dev_eui')
        self.raum_controller = RaumController()

    async def _select_stmt(self, model: Model, join_foreign_keys=False):
        if not join_foreign_keys:
            return """SELECT name, idRaum as "raum.id", art FROM sensoren WHERE dev_eui=$1"""
        else:
            return """
            SELECT sensoren.name, sensoren.art,
            raeume.id as "raum.id", raeume.name as "raum.name",
            stockwerke.id as "stockwerk.id", stockwerke.name as "stockwerk.name", stockwerke.niveau as "stockwerk.niveau",
            gebaeude.id as "gebaeude.id", gebaeude.name as "gebaeude.name"
            FROM sensoren
            LEFT JOIN raeume ON sensoren.idraum = raeume.id
            LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
            LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
            WHERE dev_eui=$1
            """

    async def _insert_stmt(self):
        return """INSERT INTO sensoren (dev_eui, name, art, idraum) VALUES ($1, $2, $3, $4)"""

    async def _insert_values(self, model: Model):
        return model["dev_eui"].value, model["name"].value, model["art"].value.value, model["raum"]["id"].value

    async def _update_stmt(self):
        return """UPDATE sensoren SET name=$2, art=$3, idraum=$4 WHERE dev_eui=$1"""

    async def _update_values(self, model: Model):
        return await self._insert_values(model)

    @property
    def identifiers(self) -> List[str]:
        """Die Dev_eui ist wie die MAC Adresse der Sensoren und ist immer eindeutig."""
        return ["dev_eui"]

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen veränderungen and Sensoren wahrnemen."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        else:
            return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Administratoren und Reinigunspersonal dürfen Sensoren anschauen. Administratoren dürfen auch Werte einlesen lassen."""
        return await self.get_permissions_for_role(requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Administratoren und Reinigunspersonal dürfen Sensoren anschauen. Administratoren dürfen auch Werte einlesen lassen."""
        if role == Roles.ADMIN.value:
            return {
                'dev_eui': Permissions.READ_WRITE,
                'name': Permissions.READ_WRITE,
                'art': Permissions.READ_WRITE,
                'raum': {
                    'id': Permissions.READ_WRITE,
                    'name': Permissions.READ
                },
                'stockwerk': {
                    'id': Permissions.READ,
                    'name': Permissions.READ,
                    'niveau': Permissions.READ
                },
                'gebaeude': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
            }
        elif role == Roles.PERSONAL.value:
            return {
                'dev_eui': Permissions.READ,
                'name': Permissions.READ,
                'art': Permissions.READ,
                'raum': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                },
                'stockwerk': {
                    'id': Permissions.READ,
                    'name': Permissions.READ,
                    'niveau': Permissions.READ
                },
                'gebaeude': {
                    'id': Permissions.READ,
                    'name': Permissions.READ
                }
            }
        return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model,
                       _type: ValidationTypes):

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['dev_eui', 'name', 'art', 'raum.id'])

            if await self.get(connection, model) is not None:
                raise ValidationError(['dev_eui'], "Sensor existiert bereits.")

        if not model["raum"]["id"].empty:
            if await self.raum_controller.get(connection, model["raum"]) is None:
                raise ValidationError(['raum.id'], "Raum existiert nicht.")

        sanitize_fields(model, ['name'])