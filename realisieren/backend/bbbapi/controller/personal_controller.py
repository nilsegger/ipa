from typing import Tuple, Dict, Any, List

from tedious.auth.auth import Requester, Auth
from tedious.mdl.model import Model, Permissions, ValidationError
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions
from tedious.sql.interface import SQLConnectionInterface
from tedious.util import create_uuid

from bbbapi.common_types import Roles
from bbbapi.models.personal import Personal
from bbbapi.util import sanitize_fields


class PersonalController(ModelController):
    """Controller für das Erstellen, Aktualisieren und Löschen von Personal."""

    def __init__(self, auth: Auth = Auth()):
        super().__init__('Personal', 'uuid')
        self.auth = auth

    async def _select_stmt(self, model: Model, join_foreign_keys=False):
        if join_foreign_keys:
            return "SELECT name, logins.username AS benutzername, logins.role AS rolle FROM Personal LEFT JOIN logins on personal.uuid = logins.uuid WHERE personal.uuid=$1"
        else:
            return "SELECT name FROM Personal WHERE uuid=$1"

    async def _insert_stmt(self):
        return "INSERT INTO Personal (uuid, name) VALUES ($1, $2)"

    async def _insert_values(self, model: Model):
        """Antwortet mit den korrekt sortieren Werten eines Personal Models für diese Erstellung."""

        return model["uuid"].value, model["name"].value

    async def _update_stmt(self):
        return "UPDATE personal SET name=coalesce($2) WHERE uuid=$1"

    async def _update_values(self, model: Model):
        """Antwortet mit den korrekt sortieren Werten eines Personal Models für die Aktualisierung."""

        return model["uuid"].value, model["name"].value

    @property
    def identifiers(self) -> List[str]:
        """Nur die UUID ist Wichtig um eine Person zu erkennen."""
        return ["uuid"]

    async def create(self, connection: SQLConnectionInterface, model: Personal):
        """Personal Models müssen nicht nur erstellt werden, sondern auch noch ein dazu passendes login haben.
        Dieses wird hier erstellt."""
        await self.validate(connection, model, ValidationTypes.CREATE)
        requester = await self.auth.register(connection, model["benutzername"].value, model["passwort"].value, model["rolle"].value.value)
        model["uuid"].value = requester.uuid
        await connection.execute(await self._insert_stmt(), *await self._insert_values(model))
        return model

    async def update(self, connection: SQLConnectionInterface, model: Model, _global: Model = None):
        """Aktualisiert Personal. Wenn Benutzername oder Passwort nicht leer ist, so wird das auch das Login aktualisiert."""
        await self.validate(connection, model, ValidationTypes.UPDATE)
        if not model["benutzername"].empty or not model["passwort"].empty or not model["rolle"].empty:
            await self.auth.update(connection, Requester(uuid=model["uuid"].value),
                                   model["benutzername"].value, model["passwort"].value,
                                   model["rolle"].value.value if not model["rolle"].empty else None)
        await connection.execute(await self._update_stmt(), *await self._update_values(model))

    async def get_manipulation_permissions(self, requester: Requester, model: Model) -> Tuple[ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen eine Person erstellen, aktualisieren oder löschen."""
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        else:
            return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Nur der Name darf eingelesen werden. Die UUID darf nie
        von einem Benutzer verändert werden."""
        return await self.get_permissions_for_role(requester.role if requester
                                                   is not None else None)

    async def get_permissions_for_role(self, role):
        """Nur der Name darf eingelesen werden. Die UUID darf nie
        von einem Benutzer verändert werden."""
        if role is not None and role == Roles.ADMIN.value:
            return {
                'uuid': Permissions.READ,
                'name': Permissions.READ_WRITE,
                'benutzername': Permissions.READ_WRITE,
                'passwort': Permissions.WRITE,
                'rolle': Permissions.READ_WRITE
            }
        else:
            return {}

    async def validate(self, connection: SQLConnectionInterface, model: Model, _type: ValidationTypes):
        """Prüft beim erstellen des Models if die UUID und der Name schon gesetzt wurde.
           Da die UUID die Login UUID referenziert kann diese nicht hier gesetzt werden."""

        if _type == ValidationTypes.CREATE:

            if model["uuid"].value is not None:
                raise ValidationError(['uuid'], "UUID can not be set in advance.")

            await model.validate_not_empty(['name', 'benutzername', 'passwort', 'rolle'])

        sanitize_fields(model, ['name', 'benutzername'])

