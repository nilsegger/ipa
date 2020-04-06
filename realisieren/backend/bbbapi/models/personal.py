from tedious.mdl.model import Model
from tedious.mdl.fields import *

from bbbapi.common_types import Roles


class Personal(Model):
    """Ein Personalmodell entspricht einer Reihe aus der Personal Tabelle.

    Felder:
        uuid, name, benutzername, passwort, rolle
    """

    def __init__(self, name: str = None, uuid=None):
        super().__init__(name, [
            UUIDField('uuid', value=uuid),
            StrField('name', min_len=3, max_len=99),
            StrField('benutzername', min_len=3, max_len=30),
            StrField('passwort', min_len=6, max_len=99),
            EnumField('rolle', enum_class=Roles)
        ])