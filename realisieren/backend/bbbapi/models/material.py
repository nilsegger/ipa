from tedious.mdl.fields import IntField, StrField
from tedious.mdl.model import Model


class Material(Model):
    """Ein Materialmodell entspricht einer Reihe aus der Materialien Tabelle.

    Felder:
        id, name, anzahl
    """

    def __init__(self, name: str=None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            StrField('name', min_len=3, max_len=99),
            IntField('anzahl')
        ])