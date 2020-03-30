from tedious.asgi.request_interface import RequestInterface
from tedious.mdl.model import Model
from tedious.res.form_resource import FormResource

from bbbapi.common_types import MeldungsArt
from bbbapi.controller.meldung_controller import MeldungController
from bbbapi.models.meldung import Meldung


class MeldungFormResource(FormResource):
    """Erweiterung der FormResource welche die Meldungs Art auf Manuell setzt."""

    async def _read_body_to_model(self, request: RequestInterface,
                                  model: Model, field_permissions):
        model = await super()._read_body_to_model(request, model,
                                                 field_permissions)
        model["art"].value = MeldungsArt.MANUELL
        model["personal"]["uuid"].value = request.requester.uuid
        return model

    def __init__(self):
        super().__init__(Meldung, MeldungController(), 'id')