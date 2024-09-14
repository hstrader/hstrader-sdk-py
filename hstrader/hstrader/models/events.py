from enum import Enum


class Event(Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"

    ORDER = "order"
    POSITION = "position"
    DEAL = "deal"

    SUMMARY = "summary"
    MARKET = "market"
    POSITION_PL = "position_pl"
    START_MARKET_FEED = "start_market_feed"
    STOP_MARKET_FEED = "stop_market_feed"
    ERROR = "bad_request"


class Status(Enum):
    CREATED = "create"
    UPDATED = "update"
    DELETED = "delete"
    CLOSED = "close"
    CANCELED = "cancel"
