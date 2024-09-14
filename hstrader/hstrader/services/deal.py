from ..models import Deal
from ..helpers import HttpClient
from ..config import Config
from .urls import _URL_GETMYDEALS
from typing import List


class DealService:

    def __init__(self, config: Config):
        self.__config: Config = config
        
    def get_deals(self) -> List[Deal]:
        """get the list of deals of the account

        Returns:
            List[Order]: list of deals of the account
        """
        response = (
            HttpClient(self.__config, url=_URL_GETMYDEALS)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        return response.deserialize_list(Deal)