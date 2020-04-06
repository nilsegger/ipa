from bbbapi.models.material import Material
from tedious.mdl.list_controller import ListController



class MaterialienListController(ListController):
    """Erstellt eine Auflistung der Materialien."""

    def __init__(self):
        super().__init__(Material)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        return """SELECT id, name FROM materialien"""
