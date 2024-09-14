from ..helpers import HttpClient
from ..config import Config
from ..models import Symbol
from typing import List
from .urls import _GETMYSYMBOLS, _GETMYSYMBOL
from .utils import apply_spread


class SymbolService:
    def __init__(self, config: Config):
        self.__config: Config = config

    def get_symbol(
        self,
        name: str,
    ) -> Symbol:
        """get the list of symbols

        Returns:
            Symbol: symbol requested
        """
        response = (
            HttpClient(self.__config, url=_GETMYSYMBOL.replace("%v", name))
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        symbol = apply_spread(response.deserialize(Symbol))
        self.__config.set_symbol(symbol)
        return symbol

    def get_symbols(
        self,
    ) -> List[Symbol]:
        """get the list of symbols

        Returns:
            List[Symbol]: the list of symbols
        """
        response = (
            HttpClient(self.__config, url=_GETMYSYMBOLS)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        symbols = [apply_spread(symbol) for symbol in response.deserialize_list(Symbol)]
        self.__config.set_symbols(symbols)
        return symbols
