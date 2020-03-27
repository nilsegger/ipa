from bbbapi.models.stockwerk import Stockwerk
from tedious.mdl.list_controller import ListController


class StockwerkeListController(ListController):
    """Erstellt eine Auflistung der Stockwerke."""

    def __init__(self):
        super().__init__(Stockwerk)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        if not join_foreign_keys:
            return """SELECT id, name, niveau, idgebaeude AS "gebaeude.id" FROM stockwerke LIMIT {} OFFSET {}""".format(limit, offset)
        else:
            return """SELECT 
                    stockwerke.id as "id", 
                    stockwerke.name as "name",
                    stockwerke.niveau,
                    gebaeude.id as "gebaeude.id",
                    gebaeude.name as "gebaeude.name"
                    FROM stockwerke
                    JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                    LIMIT {} OFFSET {}
                    """.format(limit, offset)
