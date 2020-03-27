from typing import Tuple, Dict, Any, List

from bbbapi.util import sanitize_fields
from tedious.auth.auth import Requester
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.common_types import Roles
from bbbapi.controller.gebaeude_controller import GebaeudeController

from bbbapi.controller.stockwerk_controller import StockwerkController
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions


class RaumController(ModelController):

    def __init__(self):
        super().__init__('raeume', 'id')
        self.stockwerk_controller = StockwerkController()
        self.gebaeude_controller = GebaeudeController()

    """Raum Controller für die Erstellung, Aktualisierung und Löschung von Räumen."""

    async def _select_stmt(self, model: Model, join_foreign_keys=False):

        if not join_foreign_keys:
            return "SELECT id, idStockwerk, name FROM raeume WHERE id=$1"
        else:
            return """
                SELECT 
                raeume.name as "name",
                stockwerke.id as "stockwerk.id",
                stockwerke.name as "stockwerk.name",
                stockwerke.niveau as "stockwerk.niveau",
                gebaeude.id as "gebaeude.id",
                gebaeude.name as "gebaeude.name"
                FROM raeume
                LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
                LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                WHERE raeume.id=$1
            """

    async def _insert_stmt(self):
        return "INSERT INTO raeume (id, name, idstockwerk) VALUES (DEFAULT, $1, $2) RETURNING id"

    async def _insert_values(self, model: Model):
        return model["name"].value, model["stockwerk"]["id"].value

    async def _update_stmt(self):
        return "UPDATE raeume SET name=$2, idstockwerk=$3 WHERE id=$1"

    async def _update_values(self, model: Model):
        return model["id"].value, model["name"].value, model["stockwerk"]["id"].value

    @property
    def identifiers(self) -> List[str]:
        """Der Raum wird durch die ID identifiziert."""
        return ["id"]

    async def create(self, connection: SQLConnectionInterface, model: Model):
        """Erstellt den Raum nach dem die Werte überprüft wurden."""
        await self.validate(connection, model, ValidationTypes.CREATE)
        model["id"].value = await connection.fetch_value(await self._insert_stmt(), * await self._insert_values(model))
        return model

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[
        ManipulationPermissions, Dict[str, Any]]:
        """Räume dürfen nur von Administratoren erstellt werden."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Räume dürfen von Administratoren und vom Reinigunspersonal eingesehen werden.
        Nur Administratoren dürfen jedoch Werte setzen."""
        return await self.get_permissions_for_role(requester.role if requester is not None else None)

    async def get_permissions_for_role(self, role):
        """Räume dürfen von Administratoren und vom Reinigunspersonal eingesehen werden.
                Nur Administratoren dürfen jedoch Werte setzen."""
        if role is not None and role == Roles.ADMIN.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ_WRITE,
                'gebaeude': {'id': Permissions.READ_WRITE, 'name': Permissions.READ},
                'stockwerk': {'id': Permissions.READ_WRITE, 'name': Permissions.READ, 'niveau': Permissions.READ}
            }
        elif role is not None and role == Roles.PERSONAL.value:
            return {
                'id': Permissions.READ,
                'name': Permissions.READ,
                'gebaeude': {'id': Permissions.READ, 'name': Permissions.READ},
                'stockwerk': {'id': Permissions.READ, 'name': Permissions.READ, 'niveau': Permissions.READ}
            }
        else:
            return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model,
                       _type: ValidationTypes):
        """Validiert und prüft dass der Name und die Stockwerk ID nicht leer sind.
        Die Stockwerk ID wird auch geprüft, ob diese auch wirklich korrekt ist."""

        if _type == ValidationTypes.CREATE:
            await model.validate_not_empty(['name', 'stockwerk.id'])

        if not model["stockwerk"]["id"].empty:
            stockwerk = await self.stockwerk_controller.get(connection, model["stockwerk"])
            if stockwerk is None:
                raise ValidationError(['stockwerk.id'], "Stockwerk existiert nicht.")

        sanitize_fields(model, ['name'])

