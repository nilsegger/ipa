from bbbapi.models.meldung import Meldung
from tedious.mdl.list_controller import ListController


class MeldungListController(ListController):
    """Erstellt eine Auflistung aller Meldungen."""

    def __init__(self, only_bearbeitet=False, only_not_bearbeitet=False):
        self.only_bearbeitet = only_bearbeitet
        self.only_not_bearbeitet = only_not_bearbeitet
        super().__init__(Meldung)

    async def _select_stmt(self, limit, offset, join_foreign_keys) -> str:

        if not join_foreign_keys:
            return """
                SELECT   
                id, 
                idBeobachter as "beobachter.id", 
                dev_euiSensor as "sensor.dev_eui",
                idRaum as "raum.id",
                uuidPersonal as "personal.uuid",
                art,
                datum,
                bearbeitet,
                beschreibung
                FROM meldungen
                ORDER BY datum DESC
                LIMIT {} OFFSET {}
            """.format(limit, offset)
        else:
            columns = """
                    SELECT
                    meldungen.id, 
                    meldungen.art,
                    meldungen.datum,
                    meldungen.bearbeitet,
                    meldungen.beschreibung,
                    beobachter.id as "beobachter.id",
                    beobachter.name as "beobachter.name",
                    beobachter.art as "beobachter.art",
                    beobachter.wertName as "beobachter.wertName",
                    beobachter.ausloeserWert as "beobachter.ausloeserWert",
                    beobachter.stand as "beobachter.stand",
                    sensoren.dev_eui as "sensor.dev_eui",
                    sensoren.art as "sensor.art",
                    sensoren.name as "sensor.name",
                    raeume.id as "raum.id",
                    raeume.name as "raum.name",
                    stockwerke.id as "stockwerk.id",
                    stockwerke.name as "stockwerk.name",
                    stockwerke.niveau as "stockwerk.niveau",
                    gebaeude.id as "gebaeude.id",
                    gebaeude.name as "gebaeude.name",
                    personal.uuid as "personal.uuid",
                    personal.name as "personal.name"
                    FROM meldungen
                    LEFT JOIN beobachter ON meldungen.idBeobachter = beobachter.id
                    LEFT JOIN sensoren ON meldungen.dev_euisensor = sensoren.dev_eui
                    LEFT JOIN raeume ON meldungen.idRaum = raeume.id
                    LEFT JOIN stockwerke ON raeume.idstockwerk = stockwerke.id
                    LEFT JOIN gebaeude ON stockwerke.idgebaeude = gebaeude.id
                    LEFT JOIN personal ON meldungen.uuidpersonal = personal.uuid
                        """
            orders = "ORDER BY datum DESC"
            if not self.only_bearbeitet and not self.only_not_bearbeitet:
                return "{} ORDER BY meldungen.datum DESC LIMIT {} OFFSET {}".format(
                    columns, limit, offset)
            elif self.only_not_bearbeitet:
                return "{} WHERE meldungen.bearbeitet=false {} LIMIT {} OFFSET {}".format(
                    columns, orders, limit, offset)
            else:
                return "{} WHERE meldungen.bearbeitet=true {} LIMIT {} OFFSET {}".format(
                    columns, orders, limit, offset)
