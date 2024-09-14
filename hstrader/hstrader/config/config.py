from pydantic import BaseModel
import os
from enum import IntEnum
from typing import Dict, List
from ..models import Symbol


class Strategy(IntEnum):
    """Strtegy determines the strategy to use for the communication with the server

    AUTO: the client will use the websocket if connected, otherwise it will use the http
    WS: the client will use the websocket, if not connected it will raise an error
    HTTP: the client will use the http
    """

    AUTO = 0
    WS = 1
    HTTP = 2


class Config(BaseModel):
    """Config is a class that holds the configuration for the client about the server and the communication and logging

    Args:

        timeout (int, optional): the timeout for the http requests. Defaults to 5.
        log_path (str, optional): the path of the log file. Defaults to "./logs/vertexfx.log".
        strategy (Strategy, optional): the strategy to use for the communication with the server. Defaults to Strategy.AUTO.
    """

    timeout: int
    strategy: Strategy
    disable_logging: bool
    url: str

    account_id: int = None
    access_token: str = None
    refresh_token: str = None
    session_id: str = None

    is_connected: bool = False

    symbols: Dict[int, Symbol] = {}

    def __init__(
        self,
        url: str,
        timeout: int = 5,
        disable_logging=False,
        strategy: Strategy = Strategy.AUTO,
        **kwargs
    ):

        super().__init__(
            url=url,
            timeout=timeout,
            strategy=strategy,
            disable_logging=disable_logging,
            **kwargs
        )

    def get_url(self) -> str:
        """get the base url of the server

        Returns:
            str: the base url of the server
        """
        return self.url

    def set_url(self, url: str) -> None:
        """set the base url of the server

        Args:
            url (str): the base url of the server
        """
        self.url = url

    def get_token(self) -> str:
        """get the access token

        Raises:
            ValueError: if the token is not set

        Returns:
            str: the access token
        """
        if self.access_token is None:
            raise ValueError("You need to login first to get the token")
        return self.access_token

    def set_symbols(self, symbols: List[Symbol]) -> None:
        """set the symbols

        Args:
            symbols (List[Symbol]): the symbols
        """
        self.symbols = {symbol.id: symbol for symbol in symbols}

    def set_symbol(self, symbol: Symbol) -> None:
        """set the symbol

        Args:
            symbol (Symbol): the symbol
        """
        if symbol is not None and symbol.id != 0:
            self.symbols[symbol.id] = symbol

    def get_symbols(self) -> List[Symbol]:
        """get the symbols

        Returns:
            List[Symbol]: the symbols
        """
        return self.symbols.values()

    def get_symbol(self, symbol_id: int) -> Symbol:
        """get the symbol by id

        Args:
            symbol_id (int): the symbol id

        Returns:
            Symbol: the symbol
        """
        try:
            return self.symbols[symbol_id]
        except:
            return None
