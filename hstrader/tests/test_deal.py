from . import client
from hstrader import HsTrader

def test_get_deals(client: HsTrader):
    deals = client.get_deals()
    assert len(deals) > 0
    assert deals[0].id is not None