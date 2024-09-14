from enum import IntEnum, Enum


class SideType(IntEnum):
    BUY = 0
    SELL = 1


class OrderType(IntEnum):
    MARKET = 0
    BUY_LIMIT = 1
    BUY_STOP = 2
    SELL_LIMIT = 3
    SELL_STOP = 4
    BUY_STOP_LIMIT = 5
    SELL_STOP_LIMIT = 6


class ExpirationPolicy(IntEnum):
    GOOD_TILL_CANCELED = 0
    DAY = 1
    SPECIFIED_TIME = 2
    SPECIFIED_DAY = 3


class OrderStatus(IntEnum):
    STARTED = 0
    PLACED = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 4
    REJECTED = 5
    EXPIRED = 6


class FillPolicy(IntEnum):
    FILL_OR_KILL = 0
    IMMEDIATE_OR_CANCEL = 1


class DirectionType(IntEnum):
    IN = 0
    OUT = 1


class FillType(IntEnum):
    FULL = 0
    PARTIAL = 1


class PositionStatus(IntEnum):
    OPEN = 0
    CLOSING = 1
    CLOSED = 2


class ExecutionMode(IntEnum):
    INSTANCE = 0
    REQUEST = 1
    EXECUTE = 2
    EXCHANGE = 3


class Swaptype(IntEnum):
    POINTS = 0
    BASE_CURRENCY = 1
    MARGIN_CURRENCY = 2
    DEPOSIT_CURRENCY = 3
    CURRENT_PRICE = 4
    OPEN_PRICE = 5
    REOPEN_CLOSE = 6
    REOPEN_BID = 7


class CalcType(IntEnum):

    FOREX = 0
    FOREX_NO_LEVERAGE = 1
    CONTRACTS_EXCHANGE_STOCKS = 2
    CONTRACTS_LEVERAGE = 3
    CONTRACTS_INDEX = 4
    FUTURES_EXCHANGE = 5
    EXCHANGE_BONDS = 6


class SymbolStatus(IntEnum):

    ENABLED = 0
    DISABLED = 1
    SESSIONS_CLOSED = 2
    TRADE_CLOSED_QUOTE_OPENED = 3
    TRADE_OPENED_QUOTE_CLOSED = 4
    TIMEOUTED = 5
    TIME_LIMIT_EXPIRED = 6


class TradeLevel(IntEnum):
    FULL = 0
    BUY = 1
    SELL = 2
    CLOSE = 3
    DISABLED = 4


class TradeType(IntEnum):
    REAL = 0
    DEMO = 1


class Resolution(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MN1 = "1mo"


class MarketType(Enum):
    BID = "bid"
    ASK = "ask"
