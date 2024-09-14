from . import client, EURUSD_ID
from hstrader import HsTrader
from hstrader.models import CrtOrder, OrderType, SideType, Order, UpdPosition
import pytest


@pytest.fixture
def create_position(client: HsTrader, EURUSD_ID: int) -> None:
    crt = CrtOrder(
        symbol=EURUSD_ID,
        type=OrderType.MARKET,
        side=SideType.BUY,
        volume=0.1,
        comment="test",
        order_price=0.2,
    )
    client.create_order(crt)


def test_get_position(client: HsTrader, create_position: None):
    positions = client.get_positions()
    assert len(positions) > 0


def test_update_postition(client: HsTrader, create_position: None):
    positions = client.get_positions()

    upd = UpdPosition(
        position_id=positions[0].id,
        stop_loss=0.0,
        take_profit=0.0,
        comment="test",
    )

    client.update_position(upd)


def test_close_position(client: HsTrader, create_position: None):
    positions = client.get_positions()

    client.close_position(positions[0].id, positions[0].volume)


def test_get_position_history(client: HsTrader):
    positions = client.get_position_history()
    assert len(positions) > 0
