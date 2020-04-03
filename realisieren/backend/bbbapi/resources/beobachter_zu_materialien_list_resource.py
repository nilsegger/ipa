from bbbapi.controller.beobachter_materalien_list_controller import \
    BeobachterMateralienListController
from bbbapi.models.beobachter import Beobachter

from bbbapi.common_types import Roles
from tedious.mdl.list_controller import ListController
from tedious.res.list_resource import ListResource


class MaterialienZuBeobachterListResource(ListResource):
    """Erstellt eine Auflistung von allen Materalien benötigt bei einer Meldung eines Beobachters."""

    def __init__(self, beobachter: Beobachter, limit=25):
        self.beobachter = beobachter
        super().__init__([
            Roles.ADMIN.value,
            Roles.PERSONAL.value
        ], [
            'id', 'name', 'anzahl'
        ], limit, True)

    async def get_controller(self, request, **kwargs) -> ListController:
        """Erstellt den ListController aus dem Beobachter"""

        return BeobachterMateralienListController(self.beobachter)
