from bbbapi.models.beobachter import Beobachter
from tedious.mdl.list_controller import ListController



class BeobachterListController(ListController):
    """Erstellt eine Auflistung der Beobachter."""

    def __init__(self):
        super().__init__(Beobachter)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        if not join_foreign_keys:
            return """SELECT id, name, art, dev_euiSensor as  "sensor.dev_eui", wertName as "wertName", ausloeserWert as "ausloeserWert", stand FROM beobachter"""
        else:
            return """
                SELECT beobachter.id, beobachter.name, beobachter.art, beobachter.wertName as "wertName", beobachter.ausloeserWert as "ausloeserWert", beobachter.stand,
                sensoren.dev_eui as "sensor.dev_eui", sensoren.name as "sensor.name"
                FROM beobachter
                LEFT JOIN sensoren ON beobachter.dev_euiSensor=sensoren.dev_eui 
            """
