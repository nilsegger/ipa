from typing import Tuple, Dict, Any, List

from bbbapi.util import sanitize_fields

from bbbapi.common_types import Roles
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface


class MaterialController(ModelController):
    """Controller für die Erstellung, Aktualisierung und Löschung von Materialien."""

    def __init__(self):
        super().__init__('materialien', 'id')

    async def _select_stmt(self, model: Model, join_foreign_keys=False):
        return "SELECT name FROM materialien WHERE id=$1"

    async def _insert_stmt(self):
        return "INSERT INTO materialien(name) VALUES($1) RETURNING id"

    async def _insert_values(self, model: Model):
        return model["name"].value,

    async def _update_stmt(self):
        return "UPDATE materialien SET name=coalesce($2, name) WHERE id=$1"

    async def _update_values(self, model: Model):
        return model["id"].value, model["name"].value

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt das Modell und setzt die ID."""
        await self.validate(connection, model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), *await self._insert_values(model))

    @property
    def identifiers(self) -> List[str]:
        """Ein Material wird durch die ID identifiziert."""
        return ["id"]

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[ManipulationPermissions, Dict[str, Any]]:
        """Administratoren und das Reinigungspersonal dürfen Materialien erstelle."""
        if requester is not None and requester.role in [Roles.ADMIN.value, Roles.PERSONAL.value]:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Administratoren un ddas Reinigunspersonal dürfen Werte einlesen."""
        return await self.get_permissions_for_role(requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Administratoren un ddas Reinigunspersonal dürfen Werte einlesen."""
        if role in [Roles.ADMIN.value, Roles.PERSONAL.value]:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ_WRITE
            }
        return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model,
                       _type: ValidationTypes):
        """Validiert den Namen-"""
        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['name'])

        sanitize_fields(model, ['name'])