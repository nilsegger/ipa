from typing import Tuple, Dict, Any, List

from tedious.auth.auth import Requester
from tedious.mdl.model import Model
from tedious.mdl.model_controller import ModelController, ValidationTypes, \
    ManipulationPermissions

from models.personal import Personal


class PersonalController(ModelController):
    """Controller für das Erstellen, Aktualisieren und Löschen von Personal."""

    async def _model_to_sql_values(self, model: Personal):
        """Antwortet mit den korrekt sortieren Werten eines Personal Models.

        Args:
            model: Personal Model

        Returns:
            uuid, name
        """
        return model["uuid"].value, model["name"].value

    async def _insert_stmt(self):
        pass

    async def _update_stmt(self):
        pass

    @property
    def identifiers(self) -> List[str]:
        pass

    async def get_manipulation_permissions(self, requester: Requester,
                                           model: Model) -> Tuple[
        ManipulationPermissions, Dict[str, Any]]:
        pass

    async def get_permissions(self, requester: Requester, model: Model):
        pass

    async def get_permissions_for_role(self, role):
        pass

    async def validate(self, model: Model, _type: ValidationTypes):
        pass

    def __init__(self):
        super().__init__('Personal', 'uuid')
