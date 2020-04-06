from bbbapi.models.gebaeude import Gebaeude

from bbbapi.models.stockwerk import Stockwerk
from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Raum(Model):
    """Ein Raummodell entspricht einer Reihe aus der Raeume Tabelle.

    Felder:
        id, name, stockwerk, gebaeude
    """

    def __init__(self, name: str=None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            Stockwerk('stockwerk'),
            Gebaeude('gebaeude'),
            StrField('name', min_len=3, max_len=99)
        ])