from ..config import Config, Strategy
from ..services import (
    AuthService,
    OrderService,
    PositionService,
    WebSocketService,
    SymbolService,
    AccountService,
    MarketService,
    DealService,
)
from ..models import *
from typing import Callable, Union

__version__ = "1.0.0"


class HsTrader(
    WebSocketService,
    AuthService,
    OrderService,
    PositionService,
    SymbolService,
    AccountService,
    MarketService,
    DealService,
):
    """Create a new instance client for any HS Trader server

    Args:
            client_id (str): the client id
            client_secret (str): the client secret
            url (str): the url of the broker server
            config (Config, optional): will override the default configuration. Defaults to None.
    """

    def __init__(
        self, client_id: str, client_secret: str, url: str, config: Config = None
    ) -> None:

        self.__config = config if config else Config(url=url)

        AuthService.__init__(self, self.__config)
        try:
            self.login(client_id, client_secret)
            SymbolService.__init__(self, self.__config)
            self.__config.set_symbols(self.get_symbols())
        except Exception as e:
            raise e from None
        WebSocketService.__init__(self, self.__config)
        OrderService.__init__(self, self.__config)
        PositionService.__init__(self, self.__config)
        SymbolService.__init__(self, self.__config)
        AccountService.__init__(self, self.__config)
        MarketService.__init__(self, self.__config)
        DealService.__init__(self, self.__config)

    def create_order(self, order: Union[CrtOrder, dict]) -> None:
        return self.__execute(
            WebSocketService.create_order, OrderService.create_order, order
        )

    def cancel_order(self, order_id: int) -> None:
        return self.__execute(
            WebSocketService.cancel_order, OrderService.cancel_order, order_id
        )

    def update_order(self, order: Union[UpdOrder, dict]) -> None:
        return self.__execute(
            WebSocketService.update_order, OrderService.update_order, order
        )

    def close_position(self, position_id: int, volume: float) -> None:

        return self.__execute(
            WebSocketService.close_position,
            PositionService.close_position,
            ClsPosition(position_id=position_id, volume=volume),
        )

    def update_position(self, position: Union[UpdPosition, dict]) -> None:
        return self.__execute(
            WebSocketService.update_position, PositionService.update_position, position
        )

    def __execute(self, ws_func: Callable, http_func: Callable, *args, **kwargs) -> any:
        if self.__config.strategy == Strategy.AUTO:
            if self.__config.is_connected:
                return ws_func(self, *args, **kwargs)
            else:
                return http_func(self, *args, **kwargs)

        if self.__config.strategy == Strategy.WS:
            if self.__config.is_connected:
                return ws_func(self, *args, **kwargs)
            else:
                raise ValueError(
                    "You need to connect to the websocket first, or set the strategy to AUTO"
                )

        if self.__config.strategy == Strategy.HTTP:
            return http_func(self, *args, **kwargs)

    def __login(self, identifier: str, password: str) -> None:
        self.login(identifier, password)
