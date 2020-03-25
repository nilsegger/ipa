import pytest
from bbbapi.decoders.adeunis import AdeunisDecoder


@pytest.mark.asyncio
async def test_adeunis_decoder():

    data = "af1601010e6274f9"
    expected = {
        'temperature': 22,
        'vdd': 249
    }

    # TODO vdd in % umwandeln

    decoder = AdeunisDecoder()

    assert expected == await decoder.decode(data)
