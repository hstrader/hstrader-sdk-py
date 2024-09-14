from .base import BaseModel
from typing import Union
import datetime


class WsMessage(BaseModel):
    type: str
    payload: Union[dict, None, str, int, float, bool]


class Tick(BaseModel):
    symbol_id: int
    bid: float
    ask: float
    high: float
    low: float
    close: float
    open: float
    volume: float
    time: datetime.datetime


class Summary(BaseModel):
    balance: float
    credit: float
    equity: float
    used_margin: str
    free_margin: float
    margin_level: str
    total_profit_loss: float


class PositionPL(BaseModel):
    position_id: int
    profit: float


class Error(BaseModel):
    message: str
    reason: str
