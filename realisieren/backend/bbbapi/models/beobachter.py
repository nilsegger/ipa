from bbbapi.models.gebaeude import Gebaeude

from bbbapi.models.stockwerk import Stockwerk

from bbbapi.models.raum import Raum

from bbbapi.common_types import BeobachterArt
from bbbapi.models.sensor import Sensor
from tedious.mdl.fields import *
from tedious.mdl.model import Model


class Beobachter(Model):
    """Modell welches eine Beobachter Reihe wiederspiegelt."""

    def __init__(self, name: str=None, _id=None, wert_name=None, ausloeser_wert=None, stand=None):
        super().__init__(name, [
            IntField('id', value=_id),
            Sensor('sensor'),
            Raum('raum'),
            Stockwerk('stockwerk'),
            Gebaeude('gebaeude'),
            StrField('name', min_len=3, max_len=99),
            EnumField('art', enum_class=BeobachterArt),
            StrField('wertName', value=wert_name),
            IntField('ausloeserWert', value=ausloeser_wert),
            IntField('stand', value=stand)
        ])