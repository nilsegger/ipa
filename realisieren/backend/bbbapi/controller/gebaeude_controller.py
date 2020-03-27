from typing import Tuple, Dict, Any, List

from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.common_types import Roles
from bbbapi.util import sanitize_fields


class GebaeudeController(ModelController):
    """Controller für die Verwaltung von Gebäuden."""

    def __init__(self):
        super().__init__('Gebaeude', 'id')

    async def _model_to_sql_values(self, model: Model):
        """Antwortet mit id, name."""
        return model["id"].value, model["name"].value

    async def _select_stmt(self, model: Model, fields,
                           join_foreign_keys=False):
        return "SELECT name FROM gebaeude WHERE id=$1"

    async def _insert_stmt(self):
        return "INSERT INTO Gebaeude(id, name) VALUES (DEFAULT, $1) RETURNING id"

    async def _update_stmt(self):
        return "UPDATE Gebaeude SET name=$2 WHERE id=$1"

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt ein neues Gebäude."""
        await self.validate(model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), model["name"].value)
        return model

    @property
    def identifiers(self) -> List[str]:
        """Beim Gebäude Table ist jediglich die ID wichtig."""
        return ["id"]

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[
        ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen ein Gebäude erfassen."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Administratoren dürfen den Namen einlesen.
            Aministratoren und Personal dürden den Namen auslesen."""
        return await self.get_permissions_for_role(
            requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Administratoren dürfen den Namen einlesen.
            Aministratoren und Personal dürden den Namen auslesen."""
        if role is not None and role == Roles.ADMIN.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ_WRITE
            }
        elif role is not None and role == Roles.PERSONAL.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ
            }
        return {}

    async def validate(self, model: Model, _type: ValidationTypes):

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['name'])

        sanitize_fields(model, ['name'])
