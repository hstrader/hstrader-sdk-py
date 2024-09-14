from .base import BaseModel
from .enums import SideType, DirectionType
from typing import Union


class Deal(BaseModel):

    commission: float = None
    position_id: int = None
    side: SideType = None
    stop_loss: Union[float, None] = None
    closed_volume: float = None
    open_price: float = None
    volume: float = None
    comment: str = None
    close_price: float = None
    contract_size: float = None
    external_id: str = None
    id: int = None
    swap: float = None
    direction: DirectionType = None
    external_volume: float = None
    profit: float = None
    symbol_id: int = None
    order_id: int = None
    take_profit: Union[float, None] = None
    external_price: float = None
