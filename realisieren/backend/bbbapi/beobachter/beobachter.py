from datetime import datetime
from typing import Dict, Any
import tedious.config
from bbbapi.controller.beobachter_controller import BeobachterController

from bbbapi.models.meldung import Meldung
from tedious.sql.interface import SQLConnectionInterface
from bbbapi.models.beobachter import Beobachter
from bbbapi.controller.meldung_controller import MeldungController
from bbbapi.common_types import BeobachterArt, MeldungsArt
from bbbapi.models.sensor import Sensor


async def allowed_to_post(connection: SQLConnectionInterface,
                          beobachter: Beobachter):
    """Findet die letze Meldung eines Beobachters und entscheidet ,
        ob er bereits eine neue erstellen darf.

    Args:
        connection: Verbindung zu Datenbank.
        beobachter: Beobachter Modell

    Returns:
        True, wenn der Beobachter eine neue Meldung erstellen darf, False wenn nicht.
    """
    stmt = "SELECT datum FROM meldungen WHERE idBeobachter=$1 ORDER BY datum desc LIMIT 1"
    last = await connection.fetch_value(stmt, beobachter["id"].value)
    if last is None:
        return True
    elif datetime.now().timestamp() - float(tedious.config.CONFIG["BEOBACHTER"][
        "timeout"]) > last.timestamp():
        return True
    else:
        return False


def create_meldung(beobachter, sensor, beschreibung):
    """Methode welche Hilft automatische Meldungen Modelle zu erstellen."""
    meldung = Meldung()
    meldung["beobachter"]["id"].value = beobachter["id"].value
    meldung["sensor"]["dev_eui"].value = sensor["dev_eui"].value
    meldung["raum"]["id"].value = sensor["raum"]["id"].value
    meldung["art"].value = MeldungsArt.AUTO
    meldung["beschreibung"].value = beschreibung
    return meldung


class BeobachterInterface:
    """Ein Beobachter erstellt eine Meldung wenn ein gewisser Wert überschritten wurde."""

    def __init__(self, _type: BeobachterArt):
        self.type = _type

    async def watch(self, connection: SQLConnectionInterface,
                    beobachter: Beobachter,
                    beobachter_controller: BeobachterController,
                    meldung_controller: MeldungController,
                    sensor: Sensor, payload: Dict[str, Any]):
        """Wird Aufgerufen wenn ein neuer Wert eines Sensors erhalten wurde.

        Args:
            connection: Verbindung zur Datenbank
            beobachter: Beobachter Instanz von Datenbank
            beobachter_controller: Controller für die Aktualisierung eines Beobachter.
            meldung_controller: Controller für das Erstellen einer Meldung.
            sensor: Sensor Modell
            payload: JSON Werte des Modells
        """
        raise NotImplementedError


class ZaehlerstandBeobachter(BeobachterInterface):
    """Wenn der Stand überschritten wird, so wird eine Meldung ausgelöst. Der Stand wird mit jedem Wert des Sensor inkrementiert."""

    def __init__(self):
        super().__init__(BeobachterArt.ZAEHLERSTAND)

    async def watch(self, connection: SQLConnectionInterface,
                    beobachter: Beobachter,
                    beobachter_controller: BeobachterController,
                    meldung_controller: MeldungController, sensor: Sensor,
                    payload: Dict[str, Any]):
        """Wenn der Stand überschritten wird, so wird eine Meldung ausgelöst.
        Der Stand wird mit jedem Wert des Sensor inkrementiert.

        Args:
            connection: Verbindung zur Datenbank
            beobachter: Beobachter Instanz von Datenbank
            beobachter_controller: Controller für die Aktualisierung eines Beobachter.
            meldung_controller: Controller für das Erstellen von Meldungen
            sensor: Sensor Modell
            payload: Sensor Werte in JSON
        """

        actual = beobachter["stand"].value
        trigger = beobachter["ausloeserWert"].value
        beobachter["stand"].value += 1
        if actual >= trigger:
            if await allowed_to_post(connection, beobachter):
                beschreibung = "Der Sensor '{}' hat seinen Zählerstand von '{}' überschritten.".format(
                    sensor["name"].value, trigger)
                meldung = create_meldung(beobachter, sensor, beschreibung)
                await meldung_controller.create(connection, meldung)
                beobachter["stand"].value = 0

        await beobachter_controller.update(connection, beobachter)


class RichtwertDarueberBeobachter(BeobachterInterface):
    """Wenn ein gewisser Wert überschritten wird, so wird eine Meldung ausgelöst."""

    def __init__(self):
        super().__init__(BeobachterArt.RICHTWERT_DARUEBER)

    async def watch(self, connection: SQLConnectionInterface,
                    beobachter: Beobachter,
                    beobachter_controller: BeobachterController,
                    meldung_controller: MeldungController, sensor: Sensor,
                    payload: Dict[str, Any]):
        """Wenn der Wert, welcher mit wertName identifiziert wird,
        ein definierter Wert überschreitet, wird eine Meldung ausgeschrieben.

        Args:
            connection: Verbindung zur Datenbank
            beobachter: Beobachter Instanz von Datenbank
            beobachter_controller: Controller für die Aktualisierung eines Beobachter.
            meldung_controller: Controller für das Erstellen von Meldungen
            sensor: Sensor Modell
            payload: Sensor Werte in JSON
        """

        actual = payload[beobachter["wertName"].value]
        trigger = beobachter["ausloeserWert"].value
        if actual > trigger:
            if await allowed_to_post(connection, beobachter):
                beschreibung = "Der Sensor '{}' hat seinen Richtwert von '{}' mit '{}' überschritten.".format(
                    sensor["name"].value, trigger, actual)
                meldung = create_meldung(beobachter, sensor, beschreibung)
                await meldung_controller.create(connection, meldung)


class RichtwertDarunterBeobachter(BeobachterInterface):
    """Wenn ein gewisser Wert unterschreitet wird, so wird eine Meldung ausgelöst."""

    def __init__(self):
        super().__init__(BeobachterArt.RICHTWERT_DARUNTER)

    async def watch(self, connection: SQLConnectionInterface,
                    beobachter: Beobachter,
                    beobachter_controller: BeobachterController,
                    meldung_controller: MeldungController, sensor: Sensor,
                    payload: Dict[str, Any]):
        """Wenn der Wert, welcher mit wertName identifiziert wird,
        ein definierter Wert unterschreitet, wird eine Meldung ausgeschrieben.

        Args:
            connection: Verbindung zur Datenbank
            beobachter: Beobachter Instanz von Datenbank
            beobachter_controller: Controller für die Aktualisierung eines Beobachter.
            meldung_controller: Controller für das Erstellen von Meldungen
            sensor: Sensor Modell
            payload: Sensor Werte in JSON
        """

        actual = payload[beobachter["wertName"].value]
        trigger = beobachter["ausloeserWert"].value
        if actual < trigger:
            if await allowed_to_post(connection, beobachter):
                beschreibung = "Der Sensor '{}' hat seinen Richtwert von '{}' mit '{}' unterschritten.".format(
                    sensor["name"].value, trigger, actual)
                meldung = create_meldung(beobachter, sensor, beschreibung)
                await meldung_controller.create(connection, meldung)