import pytest
from bbbapi.decoders.tabs import TabsDecoder


@pytest.mark.asyncio
async def test_tabs_decoder():
    data_door_closed = "00fc35fa25060000"
    data_door_opened = "01fc350000070000"

    decoder = TabsDecoder()

    # TODO Batterien Wert korrekt umwandeln.

    json = await decoder.decode(data_door_closed)
    assert not json['status']
    assert json['vdd'] == 85

    json = await decoder.decode(data_door_opened)
    assert json['status']
    assert json['vdd'] == 85

