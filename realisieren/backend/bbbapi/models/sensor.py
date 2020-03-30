import typing

from bbbapi.models.stockwerk import Stockwerk
from bbbapi.common_types import SensorArt
from bbbapi.models.gebaeude import Gebaeude

from bbbapi.models.raum import Raum
from tedious.mdl.fields import *
from tedious.mdl.model import Model, IOModel


class Sensor(Model):
    """Ein Sensor Modell stellt eine Reihe aus der Sensoren Tabelle dar."""

    def __init__(self, name: str=None, dev_eui=None):
        super().__init__(name, [
            StrField('dev_eui', min_len=16, max_len=16, value=dev_eui),
            EnumField('art', enum_class=SensorArt),
            StrField('name', min_len=3, max_len=99),
            Raum('raum'),
            Stockwerk('stockwerk'),
            Gebaeude('gebaeude')
        ])

