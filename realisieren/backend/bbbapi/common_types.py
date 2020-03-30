from enum import Enum


class Roles(Enum):
    """Ein Benutzer kann entweder ein Administrator oder aus dem
    Personal sein.

    ADMIN, PERSONAL
    """

    ADMIN = 'ADMIN'
    PERSONAL = 'PERSONAL'


class SensorArt(Enum):
    """Enumerierung aller benutzten Sensoren dieses Projektes.

    ADEUNIS_RF, ELSYS_ERS_CO2, TABS
    """

    ADEUNIS_RF = 'ADEUNIS_RF'
    ELSYS_ERS_CO2 = 'ELSYS_ERS_CO2'
    TABS = 'TABS'


class MeldungsArt(Enum):
    """Eine Meldung kann entweder automatisch oder manuell erstellt worden sein.
        Automatische wurde vno Beobachter erstellt.

        AUTO, MANUELL
    """

    AUTO = "AUTO"
    MANUELL = "MANUELL"


class BeobachterArt(Enum):
    """Ein Beobachter kann entweder einen Richtwert oder Zählerstand prüfen.
        Beim Richtwert unterscheidet man von darüber und darunter.
        Beim ersten muss der Wert über X liegen damit eine Meldung ausgeschriben wird und beim anderen umgekehrt.

    """

    RICHTWERT_DARUEBER = "RICHTWERT_DARUEBER"
    RICHTWERT_DARUNTER= "RICHTWERT_DARUNTER"
    ZAEHLERSTAND = "ZAEHLERSTAND"