from ..models import Account
from ..helpers import HttpClient
from ..config import Config
from .urls import _GETMYPROFILE


class AccountService:

    def __init__(self, config: Config):
        self.__config: Config = config

    def get_account(self) -> Account:
        """get the account information

        Returns:
            Account: the account information
        """
        response = (
            HttpClient(self.__config, url=_GETMYPROFILE)
            .set_authorization_header(self.__config.get_token())
            .get()
        )

        return response.deserialize(Account)
