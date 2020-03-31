import pytest
import tedious.config
from bbbapi.common_types import Roles
from tedious.auth.auth import Requester
from tedious.tests.util import TestConnection, MockLogger, MockRequest

from bbbapi.resources.material_zu_beobachter_route import \
    MaterialZuBeobachterRoute
from ..util import create_beobachter, create_material

tedious.config.load_config('config.ini')


@pytest.mark.asyncio
async def test_post_and_delete():
    resource = MaterialZuBeobachterRoute()
    logger = MockLogger()
    requester = Requester(role=Roles.ADMIN.value)
    request = MockRequest(requester, body_json={'anzahl': 5})

    beobachter = await create_beobachter()
    material = await create_material()

    async with TestConnection() as connection:
        response = await resource.on_post(request, connection, logger, beobachter=beobachter, material=material)
        assert 'id' in response.body

        await resource.on_delete(request, connection, logger,
                               material_zu_beobachter_id=response.body['id'])

