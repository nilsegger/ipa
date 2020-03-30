from bbbapi.models.sensor import Sensor
from tedious.mdl.list_controller import ListController


class SensorenListController(ListController):
    """Auflistungs Controller der Sensoren."""

    def __init__(self):
        super().__init__(Sensor)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:
        stmt = None
        if not join_foreign_keys:
            stmt = """SELECT name, idRaum as "raum.id", art FROM sensoren LIMIT {} OFFSET {}""".format(limit, offset)
        else:
            stmt = """
            SELECT sensoren.name, sensoren.art,
            raeume.id as "raum.id", raeume.name as "raum.name",
            stockwerke.id as "stockwerk.id", stockwerke.name as "stockwerk.name", stockwerke.niveau as "stockwerk.niveau",
            gebaeude.id as "gebaeude.id", gebaeude.name as "gebaeude.name"
            FROM sensoren
            LEFT JOIN raeume ON sensoren.idraum = raeume.id
            LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
            LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
            LIMIT {} OFFSET {}
            """.format(limit, offset)

        return stmt