from .base import BaseModel
from .enums import (
    ExecutionMode,
    Swaptype,
    CalcType,
    SymbolStatus,
    TradeLevel,
    FillPolicy,
)
from typing import Union


class Symbol(BaseModel):

    id: int = None
    symbol: str = None
    isin: str = None
    desc: str = None
    base_currency: str = None
    quote_currency: str = None
    leverage: int = None
    margin_initial: float = None
    margin_maintenance: float = None
    margin_buy: float = None
    margin_sell: float = None
    maintenance_margin_buy: float = None
    maintenance_margin_sell: float = None
    enabled: bool = None
    trade_level: TradeLevel = None
    execution: ExecutionMode = None
    filling: FillPolicy = None
    expiration: str = None
    min_value: float = None
    max_value: float = None
    step: float = None
    swap_mode: int = None
    swap_type: Swaptype = None
    swap_long: float = None
    swap_short: float = None
    digits: int = None
    spread: Union[float, None] = None
    spread_balance: float = None
    stop_level: float = None
    calculation: CalcType = None
    contract_size: int = None
    quote_sessions: str = None
    trade_sessions: str = None
    status: SymbolStatus = None
    last_bid: float = None
    last_ask: float = None
    open: float = None
    close: float = None
    high_bid: float = None
    low_bid: float = None
    high_ask: float = None
    low_ask: float = None
