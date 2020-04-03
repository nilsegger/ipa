from bbbapi.models.gebaeude import Gebaeude
from tedious.mdl.list_controller import ListController



class GebaeudeListController(ListController):
    """Erstellt eine Auflistung der Gebäude."""

    def __init__(self):
        super().__init__(Gebaeude)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        return """SELECT id, name FROM gebaeude"""





