from bbbapi.models.beobachter import Beobachter
from bbbapi.models.gebaeude import Gebaeude

from bbbapi.models.stockwerk import Stockwerk

from bbbapi.models.sensor import Sensor

from bbbapi.models.personal import Personal

from bbbapi.common_types import MeldungsArt
from bbbapi.models.raum import Raum
from tedious.mdl.fields import *
from tedious.mdl.model import Model, IOModel


class Meldung(Model):
    """Ein Meldungsmodell entspricht einer Reihe aus der Meldungen Tabelle.

    Felder:
        id, art, bearbeitet, beschreibung, datum, raum, beobachter, gebaeude, stockwerk,
        sensor, personal
    """

    def __init__(self, name: str = None, _id=None):
        super().__init__(name, [
            IntField('id', value=_id),
            EnumField('art', enum_class=MeldungsArt),
            Raum('raum'),
            Beobachter('beobachter'),
            Stockwerk('stockwerk'),
            Gebaeude('gebaeude'),
            Sensor('sensor'),
            Personal('personal'),
            DateTimeField('datum'),
            BoolField('bearbeitet'),
            StrField('beschreibung', max_len=5000)
        ])