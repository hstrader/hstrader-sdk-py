from .base import BaseModel
from .enums import TradeType


class Account(BaseModel):
    trade_type: TradeType = None
    balance: float = None
    free_margin: float = None
    margin_level: float = None
    used_margin: float = None
    floating_profit: float = None
    credit: float = None
    currency: str = None
    relized_profit: float = None
    profit: float = None
    leverage: int = None
    equity: float = None
    id: int = None
