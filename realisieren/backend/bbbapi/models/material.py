from tedious.mdl.fields import IntField, StrField
from tedious.mdl.model import Model


class Material(Model):
    """Modell für ein Material. Ein Material hat einen nur einen Namen und ID."""

    def __init__(self, name: str=None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            StrField('name', min_len=3, max_len=99),
            IntField('anzahl')
        ])