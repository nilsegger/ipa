from typing import Dict, Tuple, Any, List

from bbbapi.controller.gebaeude_controller import GebaeudeController

from bbbapi.util import sanitize_fields
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.common_types import Roles


class StockwerkController(ModelController):
    """Controller für die Erstellung, Aktualisierung und Löschung von Stockwerk Controllern."""

    def __init__(self):
        super().__init__('stockwerke', 'id')
        self.gebaude_controller = GebaeudeController()

    async def _insert_stmt(self):
        return "INSERT INTO stockwerke (id, idgebaeude, name, niveau) VALUES (DEFAULT, $1, $2, $3) RETURNING id"

    async def _insert_values(self, model: Model):
        return model["gebaeude"]["id"].value, model["name"].value, model["niveau"].value

    async def _update_stmt(self):
        return "UPDATE stockwerke SET idgebaeude=coalesce($2, idgebaeude), name=coalesce($3, name), niveau=coalesce($4, niveau) WHERE id=$1"

    async def _update_values(self, model: Model):
        return model["id"].value, model["gebaeude"]["id"].value, model["name"].value, model["niveau"].value

    async def _select_stmt(self, model: Model, join_foreign_keys=False):
        if not join_foreign_keys:
            return """SELECT idGebaeude AS "gebaeude.id", name, niveau FROM stockwerke WHERE id=$1"""
        else:
            return """SELECT 
                        stockwerke.name, stockwerke.niveau, 
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
        await self.validate(connection, model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), *await self._insert_values(model))
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
                'name': Permissions.READ_WRITE,
                'niveau': Permissions.READ_WRITE,
            }
        elif role is not None and role == Roles.PERSONAL.value:
            return {
                'id': Permissions.READ,
                'gebaeude': {
                    'id': Permissions.READ
                },
                'name': Permissions.READ,
                'niveau': Permissions.READ
            }
        else:
            return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model, _type: ValidationTypes):
        """Prüft dass alle Werte gegeben sind. Zudem wird hier geschaut, dass die Gebäude ID korrekt ist."""

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['gebaeude.id', 'name', 'niveau'])

        if not model["gebaeude"].empty:
            if await self.gebaude_controller.get(connection, model["gebaeude"]) is None:
                raise ValidationError(['gebaeude.id'], "Das gegebene Gebäude existiert nicht.")

        sanitize_fields(model, ['name'])

