from bbbapi.models.gebaeude import Gebaeude
from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Stockwerk(Model):
    """Ein Stockwerkmodell entspricht einer Reihe aus der Stockwerke Tabelle.

    Felder:
        id, name, niveau, gebaeude
    """

    def __init__(self, name: str = None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            Gebaeude('gebaeude'),
            StrField('name', min_len=3, max_len=99),
            IntField('niveau')
        ])