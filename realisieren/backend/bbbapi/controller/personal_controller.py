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
    """Controller für das Erstellen, Aktualisieren und Löschen von Personalmodellen."""

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
        return model["uuid"].value, model["name"].value

    async def _update_stmt(self):
        return "UPDATE personal SET name=coalesce($2) WHERE uuid=$1"

    async def _update_values(self, model: Model):
        return model["uuid"].value, model["name"].value

    async def _delete_stmt(self):
        return """DELETE FROM logins WHERE uuid=$1"""

    @property
    def identifiers(self) -> List[str]:
        """Ein Personal Modell wird durch die UUID identifiziert."""
        return ["uuid"]

    async def create(self, connection: SQLConnectionInterface, model: Personal):
        """Erstellt das Personal Modell und aktiviert sein Login.

        Args:
            connection: Verbindung zu Datenbank.
            model: Personal Model.

        Returns:
            Personal Modell.
        """

        await self.validate(connection, model, ValidationTypes.CREATE)
        requester = await self.auth.register(connection, model["benutzername"].value, model["passwort"].value, model["rolle"].value.value)
        model["uuid"].value = requester.uuid
        await connection.execute(await self._insert_stmt(), *await self._insert_values(model))
        return model

    async def update(self, connection: SQLConnectionInterface, model: Model, _global: Model = None):
        """Aktualisiert das Personal und wenn nötig auch das Login.

        Args:
            connection: Verbindung zur Datenbank.
            model: Personal Model
            _global: Datenbank Kopie des Modells

        Returns:
            Personal Modell.
        """
        await self.validate(connection, model, ValidationTypes.UPDATE)
        if not model["benutzername"].empty or not model["passwort"].empty or not model["rolle"].empty:
            await self.auth.update(connection, Requester(uuid=model["uuid"].value),
                                   model["benutzername"].value, model["passwort"].value,
                                   model["rolle"].value.value if not model["rolle"].empty else None)
        await connection.execute(await self._update_stmt(), *await self._update_values(model))

    async def get_manipulation_permissions(self, requester: Requester, model: Model) -> Tuple[ManipulationPermissions, Dict[str, Any]]:
        """Nur Administratoren dürfen eine Person erstellen, aktualisieren oder löschen.

        Args:
            requester: Benutzer welcher auf die API zugreift.
            model: Modell für welches die Permissions abgefragt werden.

        Returns:
            Ein Tuple mit der Manipulation Permission an erster Stelle.
        """
        if requester is not None and requester.role == Roles.ADMIN.value:
            return ManipulationPermissions.CREATE_UPDATE_DELETE, {}
        else:
            return ManipulationPermissions.NONE, {}

    async def get_permissions(self, requester: Requester, model: Model):
        """Erstellt ein Dict mit den Permissions für jedes Feld.

        Args:
            requester: Benutzer welcher auf die API zugreift.
            model: Modell für welches die Permissions abgefragt werden.

        Returns:
            Ein Dict mit feld:permission.
        """
        return await self.get_permissions_for_role(requester.role if requester
                                                   is not None else None)

    async def get_permissions_for_role(self, role):
        """Erstellt ein Dict mit den Permissions für jedes Feld.

        Args:
            requester: Benutzer welcher auf die API zugreift.
            model: Modell für welches die Permissions abgefragt werden.

        Returns:
            Ein Dict mit feld:permission.
        """

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
        """Validiert ob die UUID bereits gesetzt wurde vor dem Erstellen.
        Dies ist nicht erlaubt. Zudem wird der Inhalt auf HTML Tags geprüft.

        Args:
            connection: Verbindung zur Datenbank.
            model: Personal Modell.
            _type: Art der Validierung.
        """

        if _type == ValidationTypes.CREATE:

            if model["uuid"].value is not None:
                raise ValidationError(['uuid'], "UUID can not be set in advance.")

            await model.validate_not_empty(['name', 'benutzername', 'passwort', 'rolle'])

            stmt = "SELECT uuid FROM logins WHERE username=$1 LIMIT 1"
            if await connection.fetch_row(stmt, model["benutzername"].value) is not None:
                raise ValidationError(['benutzername'], "Benutzername existiert bereits.")
        elif _type == ValidationTypes.UPDATE:
            stmt = "SELECT uuid FROM logins WHERE uuid!=$1 AND username=$2 LIMIT 1"
            if await connection.fetch_row(stmt, model["uuid"].value, model[
                "benutzername"].value) is not None:
                raise ValidationError(['benutzername'],
                                      "Benutzername existiert bereits.")

        sanitize_fields(model, ['name', 'benutzername'])

