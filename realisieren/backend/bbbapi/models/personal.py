from tedious.mdl.model import Model
from tedious.mdl.fields import *

from bbbapi.common_types import Roles


class Personal(Model):
    """Wiederspiegelt eine Person aus dem Reinigungspersonal oder der
    Administratorgruppe.
    """

    def __init__(self, name: str = None, uuid=None):
        super().__init__(name, [
            UUIDField('uuid', value=uuid),
            StrField('name', min_len=3, max_len=99),
            StrField('benutzername', min_len=3, max_len=30),
            StrField('passwort', min_len=6, max_len=99),
            EnumField('rolle', enum_class=Roles)
        ])