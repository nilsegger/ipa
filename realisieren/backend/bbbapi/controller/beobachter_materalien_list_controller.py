from bbbapi.models.beobachter import Beobachter

from bbbapi.models.material import Material
from tedious.mdl.list_controller import ListController


class BeobachterMateralienListController(ListController):
    """Erstellt eine Auflistung von allen Materalien benötigt bei einer Meldung eines Beobachters."""

    def __init__(self, beobachter: Beobachter):
        super().__init__(Material)
        self.beobachter = beobachter

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

       return """
            SELECT materialzubeobachter.id as "id", anzahl, materialien.name as "name" FROM materialzubeobachter LEFT JOIN materialien on materialzubeobachter.idmaterial = materialien.id
            WHERE idbeobachter=$1
       """

    async def _select_values(self):
        return self.beobachter["id"].value,