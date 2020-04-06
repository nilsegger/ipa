from tedious.mdl.model import Model
from tedious.mdl.fields import *

class SensorWert(Model):
    """Ein Sensorwertmodell entspricht einer Reihe aus der SensorenWerte Tabelle.

    Felder:
        id, dekodiertJSON, erhalten
    """

    def __init__(self, name: str=None):
        super().__init__(name, [
            IntField('id'),
            StrField('dekodiertJSON'),
            DateTimeField('erhalten'),
        ])


