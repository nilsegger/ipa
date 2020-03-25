from enum import Enum


class Roles:
    """Ein Benutzer kann entweder ein Administrator oder aus dem
    Personal sein.

    ADMIN, PERSONAL
    """
    ADMIN = 'ADMIN'
    PERSONAL = 'PERSONAL'


class SensorTypes(Enum):
    """Enumerierung aller benutzten Sensoren dieses Projektes.

    ADEUNIS_RF, ELSYS_ERS_CO2, TABS
    """
    ADEUNIS_RF = 'ADEUNIS_RF'
    ELSYS_ERS_CO2 = 'ELSYS_ERS_CO2'
    TABS = 'TABS'
