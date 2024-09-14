from . import client, EURUSD_ID
from hstrader import HsTrader
import pytest
from hstrader.models import CrtOrder, OrderType, SideType, Order, UpdOrder
from typing import List


@pytest.fixture
def create_order(client: HsTrader, EURUSD_ID: int) -> None:
    crt = CrtOrder(
        symbol=EURUSD_ID,
        type=OrderType.BUY_LIMIT,
        side=SideType.BUY,
        volume=0.1,
        take_profit=99,
        stop_loss=0.2,
        comment="test",
        order_price=0.2,
    )
    client.create_order(crt)


@pytest.fixture
def test_get_orders(client: HsTrader, create_order: None) -> List[Order]:
    orders = client.get_orders()
    assert len(orders) > 0

    return orders


@pytest.fixture
def test_update_order(client: HsTrader, test_get_orders: List[Order]) -> List[Order]:
    orders = test_get_orders
    order_id = orders[0].id
    upd = UpdOrder(
        volume=0.2,
        comment="updating order",
        order_limit_price=1.2,
        stop_loss=0,
        take_profit=99,
        type=orders[0].type,
        order_id=order_id,
    )

    client.update_order(upd)

    return orders


def test_cancel_order(
    client: HsTrader,
    test_update_order: List[Order],
):
    orders = test_update_order
    order_id = orders[0].id
    client.cancel_order(order_id)


def test_get_orders_history(client: HsTrader):
    orders = client.get_orders_history()
    assert len(orders) > 0
