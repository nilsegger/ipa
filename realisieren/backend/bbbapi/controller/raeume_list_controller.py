from bbbapi.models.raum import Raum
from tedious.mdl.list_controller import ListController



class RaeumeListController(ListController):
    """Erstellt eine Auflistung der Räume."""

    def __init__(self):
        super().__init__(Raum)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        if not join_foreign_keys:
            return """SELECT id, name, idStockwerk AS "stockwerk.id" FROM raeume LIMIT {} OFFSET {}""".format(limit, offset)
        else:
            return """
                SELECT
                raeume.id AS "id",
                raeume.name as "name",
                stockwerke.id as "stockwerk.id",
                stockwerke.name as "stockwerk.name",
                stockwerke.niveau as "stockwerk.niveau",
                gebaeude.id as "gebaeude.id",
                gebaeude.name as "gebaeude.name"
                FROM raeume
                LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
                LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                LIMIT {} OFFSET {}
            """.format(limit, format)
