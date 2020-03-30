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