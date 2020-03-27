from typing import Dict, Tuple, Any, List

from bbbapi.util import sanitize_fields
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.common_types import Roles


class StockwerkController(ModelController):
    """Controller für die Erstellung, Aktualisierung und Löschung von Stockwerk Controllern."""

    def __init__(self):
        super().__init__('stockwerke', 'id')

    async def _model_to_sql_values(self, model: Model):
        return model["id"].value, model["gebaeude"]["id"].value, model["name"].value

    async def _insert_stmt(self):
        return "INSERT INTO stockwerke (id, idgebaeude, name) VALUES (DEFAULT, $1, $2) RETURNING id"

    async def _update_stmt(self):
        return "UPDATE stockwerke SET idgebaeude=$2, name=$3 WHERE id=$1"

    async def _select_stmt(self, model: Model, fields,
                           join_foreign_keys=False):
        if not join_foreign_keys:
            return """SELECT idGebaeude AS "gebaeude.id", name FROM stockwerke WHERE id=$1"""
        else:
            return """SELECT 
                        stockwerke.name, 
                        gebaeude.id AS "gebaeude.id", 
                        gebaeude.name as "gebaeude.name"
                        FROM stockwerke
                        LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                        WHERE stockwerke.id=$1
                        """

    @property
    def identifiers(self) -> List[str]:
        """Für ein Stockwerk ist die eigene ID der Identifier."""
        return ["id"]

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt das Stockwerk und setzt die automatisch inkrementierte ID."""
        await self.validate(model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), model["gebaeude"]["id"].value,
            model["name"].value)
        return model

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen ein Stockwerk erstellen."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        else:
            return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Administratoren dürfen das Gebäude und der Name setzen. Administratoren und das Reinigungspersonal dürfen alle Werte sehen."""
        return await self.get_permissions_for_role(requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Administratoren dürfen das Gebäude und der Name setzen. Administratoren und das Reinigungspersonal dürfen alle Werte sehen."""
        if role is not None and role == Roles.ADMIN.value:
            return {
                'id': Permissions.READ,
                'gebaeude': {
                    'id': Permissions.READ_WRITE
                },
                'name': Permissions.READ_WRITE
            }
        elif role is not None and role == Roles.PERSONAL.value:
            return {
                'id': Permissions.READ,
                'gebaeude': {
                    'id': Permissions.READ
                },
                'name': Permissions.READ
            }
        else:
            return {}

    async def validate(self, model: Model, _type: ValidationTypes):

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['gebaeude.id', 'name'])

        # todo validate gebaude exusts

        sanitize_fields(model, ['name'])

