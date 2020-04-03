from typing import List

from bbbapi.common_types import Roles
from tedious.mdl.list_controller import ListController
from tedious.res.list_resource import ListResource

from bbbapi.controller.meldung_list_controller import MeldungListController


class MeldungenListResource(ListResource):
    """Erstellt den Meldung List Controller und setzt die Parameter nach der gewünschten Aktion des Benutzers.

    Ist type in den Query Parametern vorhanden, so wird beim Wert bearbeitet nur nach Meldungen mit der Spalte bearbeitet auf True gesucht, sonst false.
    """

    def __init__(self, limit=25):
        super().__init__([
            Roles.ADMIN.value,
            Roles.PERSONAL.value
        ], [
            'id', 'bearbeitet', 'beschreibung', 'art', 'datum', 'sensor.dev_eui', 'sensor.name',
            'raum.id', 'raum.name', 'stockwerk.id', 'stockwerk.niveau', 'stockwerk.name',
            'gebaeude.id', 'gebaeude.name', 'beobachter.id', 'beobachter.name', 'personal.uuid', 'personal.name'
        ], limit,
            True)

    async def get_controller(self, request, **kwargs) -> ListController:
        _type = request.get_param('type')

        if _type is None:
            return MeldungListController()
        elif _type == 'bearbeitet':
            return MeldungListController(only_bearbeitet=True)
        else:
            return MeldungListController(only_not_bearbeitet=True)
