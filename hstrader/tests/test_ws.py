from . import client, unauthenticated_client, EURUSD_ID
from hstrader import HsTrader
import pytest
from hstrader.models import (
    CrtOrder,
    OrderType,
    SideType,
    Order,
    UpdOrder,
    Event,
    Status,
)


def test_ws_start(client: HsTrader):
    @client.subscribe(Event.CONNECT)
    def on_connect():
        assert True
        client.stop()

    client.start()


def test_ws_stop(client: HsTrader):
    @client.subscribe(Event.CONNECT)
    def on_connect():
        client.stop()

    @client.subscribe(Event.DISCONNECT)
    def on_disconnect():
        assert True

    client.start()
    with pytest.raises(ValueError):
        client.stop()


# def test_ws_order(client: HsTrader, EURUSD_ID: int):
#     @client.subscribe(Event.ORDER)
#     def on_order(order: Order, status: Status):

#         if status == Status.CREATED:
#             upd = UpdOrder(
#                 volume=0.2,
#                 comment="updating order",
#                 order_limit_price=1.2,
#                 stop_loss=0,
#                 take_profit=99,
#                 type=order.type,
#                 order_id=order.id,
#             )
#             client.update_order(upd)
#         elif status == Status.UPDATED:
#             client.cancel_order(order.id)
#         elif status == Status.CANCELED:
#             assert True
#             client.stop()

#     @client.subscribe(Event.CONNECT)
#     def on_connect():
#         crt = CrtOrder(
#             symbol_id=EURUSD_ID,
#             type=OrderType.BUY_LIMIT,
#             side=SideType.BUY,
#             volume=0.1,
#             take_profit=99,
#             stop_loss=0.2,
#             comment="test",
#             order_price=0.2,
#         )
#         client.create_order(crt)

#     @client.subscribe(Event.DISCONNECT)
#     def on_disconnect():
#         assert True

#     client.start()

#     with pytest.raises(ValueError):
#         client.stop()
