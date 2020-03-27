from bbbapi.models.gebaeude import Gebaeude

from bbbapi.models.stockwerk import Stockwerk
from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Raum(Model):
    """Modell für die Datenhaltung von Räumen."""

    def __init__(self, name: str=None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            Stockwerk('stockwerk'),
            Gebaeude('gebaeude'),
            StrField('name', min_len=3, max_len=99)
        ])