from tedious.mdl.model import Model
from tedious.mdl.fields import *

class SensorWert(Model):
    """Modell einer Reihe aus der SensorWerte Tabelle."""

    def __init__(self, name: str=None):
        super().__init__(name, [
            IntField('id'),
            StrField('dekodiertJSON'),
            DateTimeField('erhalten'),
        ])


