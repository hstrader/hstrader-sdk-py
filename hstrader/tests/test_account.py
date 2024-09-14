from . import client, unauthenticated_client
from hstrader import HsTrader


def test_get_account_info(
    client: HsTrader,
):
    account = client.get_account()
    assert account.id is not None
