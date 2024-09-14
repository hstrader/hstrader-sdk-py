from . import client, unauthenticated_client
from hstrader import HsTrader
import pytest


def test_get_symbols(client: HsTrader):
    symbols = client.get_symbols()
    assert symbols is not None
    assert len(symbols) > 0

def test_get_symbol(client: HsTrader):
    symbols = client.get_symbol("Ripple")
    assert symbols is not None
    assert symbols.id != None or symbols.id != 0
    with pytest.raises(Exception):
        client.get_symbol("DOESNOTEXIST")
