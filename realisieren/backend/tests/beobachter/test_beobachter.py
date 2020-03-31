import pytest
import tedious.config
from bbbapi.models.sensor import Sensor

from bbbapi.controller.beobachter_controller import BeobachterController
from tedious.mdl.model import Model
from tedious.sql.interface import SQLConnectionInterface

from bbbapi.controller.meldung_controller import MeldungController

from bbbapi.models.beobachter import Beobachter
from tedious.tests.util import TestConnection

from bbbapi.beobachter.beobachter import ZaehlerstandBeobachter, \
    RichtwertDarueberBeobachter, RichtwertDarunterBeobachter

tedious.config.load_config('config.ini')


class MockMeldungController(MeldungController):
    """Anstatt die Meldung in die Datenbank zu schreiben, inkrementiert es einen Zähler."""

    def __init__(self):
        super().__init__()
        self.counter = 0

    async def create(self, connection: SQLConnectionInterface, model: Model):
        self.counter += 1


class MockBeobachterController(BeobachterController):
    """Überschreibt Update damit Datenbank nicht abgefragt wird."""

    async def update(self, connection: SQLConnectionInterface, model: Model,
                     _global: Model = None):
        pass


@pytest.mark.asyncio
async def test_zaehlerstand():
    async with TestConnection() as connection:
        beobachter = ZaehlerstandBeobachter()
        meldung_controller = MockMeldungController()
        beobachter_controller = MockBeobachterController()
        sensor = Sensor()
        payload = {}

        await beobachter.watch(connection, Beobachter(stand=3, ausloeser_wert=4), beobachter_controller, meldung_controller, sensor, payload)
        assert meldung_controller.counter == 0

        await beobachter.watch(connection,
                               Beobachter(stand=4, ausloeser_wert=4),
                               beobachter_controller, meldung_controller,
                               sensor, payload)

        assert meldung_controller.counter == 1


@pytest.mark.asyncio
async def test_richtwert_darueber():
    async with TestConnection() as connection:
        beobachter = RichtwertDarueberBeobachter()
        meldung_controller = MockMeldungController()
        beobachter_controller = MockBeobachterController()
        sensor = Sensor()

        await beobachter.watch(connection, Beobachter(wert_name='temperatur', ausloeser_wert=5), beobachter_controller, meldung_controller, sensor, {'temperatur': 5})

        assert meldung_controller.counter == 0

        await beobachter.watch(connection, Beobachter(wert_name='temperatur',
                                                      ausloeser_wert=5),
                               beobachter_controller, meldung_controller,
                               sensor, {'temperatur': 6})

        assert meldung_controller.counter == 1


@pytest.mark.asyncio
async def test_richtwert_darunter():
    async with TestConnection() as connection:
        beobachter = RichtwertDarunterBeobachter()
        meldung_controller = MockMeldungController()
        beobachter_controller = MockBeobachterController()
        sensor = Sensor()

        await beobachter.watch(connection, Beobachter(wert_name='temperatur', ausloeser_wert=5), beobachter_controller, meldung_controller, sensor, {'temperatur': 5})

        assert meldung_controller.counter == 0

        await beobachter.watch(connection, Beobachter(wert_name='temperatur',
                                                      ausloeser_wert=5),
                               beobachter_controller, meldung_controller,
                               sensor, {'temperatur': 4})

        assert meldung_controller.counter == 1