import pytest
from hstrader import HsTrader
import os

CLIENT_ID = os.getenv("TEST_CLIENT_ID")
CLIENT_SECRET = os.getenv("TEST_CLIENT_SECRET")
URL = os.getenv("TEST_URL")


def test_vfx12():
    # load the environment variables
    assert CLIENT_ID is not None
    assert CLIENT_SECRET is not None
    assert URL is not None
    assert HsTrader(CLIENT_ID, CLIENT_SECRET, URL) is not None


@pytest.fixture
def unauthenticated_client() -> HsTrader:
    return HsTrader("", "", URL)


@pytest.fixture
def client() -> HsTrader:
    hstrader = HsTrader(CLIENT_ID, CLIENT_SECRET, URL)
    return hstrader


@pytest.fixture
def EURUSD_ID(
    client: HsTrader,
) -> int:
    return client.get_symbol("EURUSD").id
