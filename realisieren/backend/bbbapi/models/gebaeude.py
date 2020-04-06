from tedious.mdl.model import Model
from tedious.mdl.fields import *


class Gebaeude(Model):
    """Ein Gebaeudemodell entspricht einer Reihe aus der Gebaeude Tabelle.

    Felder:
        id, name
    """

    def __init__(self, name: str = None, _id: int = None):
        super().__init__(name, [
            IntField('id', value=_id),
            StrField('name', min_len=3, max_len=99)
        ])
