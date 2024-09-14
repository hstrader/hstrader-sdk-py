from .base import BaseModel
from .enums import (
    ExpirationPolicy,
    OrderStatus,
    FillPolicy,
    OrderType,
    FillType,
    SideType,
    DirectionType,
)
from .symbol import Symbol
from typing import Union
from .utils import str_to_side_type, str_to_order_type


class Order(BaseModel):

    trigger_price: Union[float, None] = None
    order_limit_price: Union[float, None] = None
    order_price: Union[float, None] = None
    order_new_price: Union[float, None] = None
    contract_size: Union[float, None] = None
    expiry_at: Union[int, None] = None
    volume: Union[float, None] = None
    expiration_policy: ExpirationPolicy = None
    status: OrderStatus = None
    filled_volume: Union[float, None] = None
    comment: Union[str, None] = None
    created_at: Union[int, None] = None
    external_volume: Union[float, None] = None
    stop_loss: Union[float, None] = None
    symbol_id: Union[int, None] = None
    external_id: Union[str, None] = None
    external_price: Union[float, None] = None
    fill_policy: FillPolicy = None
    type: OrderType = None
    fill_type: FillType = None
    side: SideType = None
    updated_at: Union[int, None] = None
    id: Union[int, None] = None
    take_profit: Union[float, None] = None
    direction: DirectionType = None
    done_at: Union[int, None] = None
    filled_price: Union[float, None] = None


class CrtOrder(BaseModel):

    type: OrderType
    volume: float
    comment: Union[str, None] = None
    order_price: Union[float, None]
    side: SideType
    stop_loss: Union[float, None] = None
    take_profit: Union[float, None] = None
    symbol_id: int

    def __init__(
        self,
        symbol: Union[int, Symbol],
        volume: float,
        side: Union[SideType, str],
        type: Union[OrderType, str],
        order_price: float,
        take_profit: Union[float, None] = None,
        stop_loss: Union[float, None] = None,
        comment: str = None,
        **data
    ):
        if isinstance(symbol, Symbol):
            symbol = symbol.id
        if isinstance(side, str):
            side = str_to_side_type(side)
        if isinstance(type, str):
            type = str_to_order_type(type)

        super().__init__(
            symbol_id=symbol,
            order_price=order_price,
            volume=volume,
            side=side,
            type=type,
            take_profit=take_profit,
            stop_loss=stop_loss,
            **data
        )


class UpdOrder(BaseModel):

    volume: Union[float, None]
    comment: Union[str, None] = None
    order_limit_price: Union[float, None] = None
    stop_loss: Union[float, None] = None
    take_profit: Union[float, None] = None
    type: Union[OrderType, None] = None
    order_id: int

    def __init__(
        self,
        order_id: int,
        volume: float = None,
        take_profit: Union[float, None] = None,
        stop_loss: Union[float, None] = None,
        order_limit_price: Union[float, None] = None,
        type: [OrderType, str, None] = None,
        comment: str = None,
        **data
    ):
        if isinstance(type, str):
            type = str_to_order_type(type)

        super().__init__(
            order_id=order_id,
            volume=volume,
            take_profit=take_profit,
            stop_loss=stop_loss,
            order_limit_price=order_limit_price,
            type=type,
            comment=comment,
            **data
        )


class CnlOrder(BaseModel):
    order_id: int

    def __init__(self, order_id: int, **data):
        super().__init__(order_id=order_id, **data)
