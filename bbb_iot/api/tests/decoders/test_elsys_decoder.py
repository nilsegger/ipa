import pytest
from bbbapi.decoders.elsys import ElsysDecoder


@pytest.mark.asyncio
async def test_elsys_decoder():

    data = "0100f1021d0400c0050006024a070e40"

    expected = {
        "temperature": 24.1,
        "humidity": 29,
        "light": 192,
        "motion": 0,
        "co2": 586,
         "vdd": 3648
    }

    # TODO Batterie Vdd muss noch in Prozent umgerechnet werden.

    decoder = ElsysDecoder()
    assert expected == await decoder.decode(data)
