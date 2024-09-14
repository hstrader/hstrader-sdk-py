from .enums import SideType, OrderType


def str_to_side_type(side: str) -> SideType:
    side = side.lower()
    mapping = {
        "buy": SideType.BUY,
        "sell": SideType.SELL,
    }

    try:
        return mapping[side]
    except KeyError:
        raise ValueError(
            "Invalid side type, must be one of {}".format(list(mapping.keys()))
        )


def str_to_order_type(order_type: str) -> OrderType:
    order_type = order_type.lower()
    mapping = {
        "market": OrderType.MARKET,
        "buy_limit": OrderType.BUY_LIMIT,
        "sell_limit": OrderType.SELL_LIMIT,
        "buy_stop": OrderType.BUY_STOP,
        "sell_stop": OrderType.SELL_STOP,
        "buy_stop_limit": OrderType.BUY_STOP_LIMIT,
        "sell_stop_limit": OrderType.SELL_STOP_LIMIT,
    }

    try:
        return mapping[order_type]
    except KeyError:
        raise ValueError(
            "Invalid order type , must be one of {}".format(list(mapping.keys()))
        )
