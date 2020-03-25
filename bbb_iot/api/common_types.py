from enum import Enum


class SensorTypes(Enum):
    """Enumerierung aller benutzten Sensoren dieses Projektes.

    ADEUNIS_RF, ELSYS_ERS_CO2, TABS
    """
    ADEUNIS_RF = 0
    ELSYS_ERS_CO2 = 1
    TABS = 2
