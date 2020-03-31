from tedious.mdl.model import Permissions

from bbbapi.common_types import Roles

from bbbapi.controller.material_controller import MaterialController

from bbbapi.controller.beobachter_controller import BeobachterController

from bbbapi.models.material import Material

from bbbapi.models.beobachter import Beobachter
from tedious.asgi.request_interface import RequestInterface
from tedious.asgi.resource_interface import ResourceInterface
from tedious.asgi.response_interface import ResponseInterface, \
    SuccessfulResponse, JSONResponse
from tedious.logger import Logger
from tedious.sql.interface import SQLConnectionInterface


class MaterialZuBeobachterRoute(ResourceInterface):
    """Fügt ein Material einem Beobachter hinzu und löscht diese Verbindung."""

    def __init__(self) -> None:
        self.beobachter_controller = BeobachterController()
        self.material_controller = MaterialController()

    async def on_post(self, request: RequestInterface,
                      connection: SQLConnectionInterface, logger: Logger,
                      beobachter: Beobachter=None, material: Material=None) -> ResponseInterface:
        """Fügt ein Material einem Beobachter hinzu

        Args:
            request: Route request
            connection: Verbindung zu Datenbank
            logger: -
            beobachter: Beobachter zu welchem das Material hinzugefügt wird
            material: Materiall welches dem Beobachter hinzugefügt wird.
        """

        if request.requester is None or request.requester.role not in [Roles.ADMIN.value, Roles.PERSONAL.value]:
            self.raise_forbidden("Bitte melden Sie sich an um diese Resource zu benutzen.")

        if await self.beobachter_controller.get(connection, beobachter) is None:
            self.raise_not_found("Beobachter konnte nicht gefunden werden.")
        elif await self.material_controller.get(connection, material) is None:
            self.raise_not_found("Material konnte nicht gefunden werden.")

        await material.input(await request.get_body_json(), {'anzahl': Permissions.WRITE}, validate_fields=['anzahl'])
        _id = await self.beobachter_controller.add_material(connection, beobachter, material)
        return JSONResponse({'id': _id})

    async def on_delete(self, request: RequestInterface,
                        connection: SQLConnectionInterface, logger: Logger, material_zu_beobachter_id=None) -> ResponseInterface:
        """Löscht ein Material einem Beobachter hinzu

                Args:
                    request: Route request
                    connection: Verbindung zu Datenbank
                    logger: -
                    material_zu_beobachter_id: ID der Verbindung welch egelöscht werden soll.
                """

        if request.requester is None or request.requester.role not in [Roles.ADMIN.value, Roles.PERSONAL.value]:
            self.raise_forbidden("Bitte melden Sie sich an um diese Resource zu benutzen.")

        await self.beobachter_controller.remove_material(connection, material_zu_beobachter_id)
        return SuccessfulResponse()