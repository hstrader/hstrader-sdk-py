import base64

from ..helpers import HttpClient
from ..config import Config
from ..models import *
from .urls import _LOGIN_URL_CREDENTIALS, _LOGOUT_URL, _REFRESH_URL


class AuthService:
    def __init__(self, config: Config):
        self.__config: Config = config

    def login(self, username: str, password: str) -> AuthResponse:
        """login to hstrader

        Args:
            username (str): username or email
            password (str): password

        Returns:
            AuthResponse: the credentials
        """

        encoded = base64.b64encode(bytes(f"{username}:{password}", "utf-8"))
        headers = {
            "Authorization": "Basic " + encoded.decode("utf-8"),
        }
        response = (
            HttpClient(
                self.__config,
                url=_LOGIN_URL_CREDENTIALS,
            )
            .set_headers(headers)
            .post()
        )

        login = response.deserialize(AuthResponse)
        self.__load_credentials(login)
        return login

    def logout(self) -> None:
        """logout from hstrader

        Raises:
            ValueError: if access token is missing
        """

        (
            HttpClient(self.__config, url=_LOGOUT_URL)
            .set_authorization_header(self.__config.get_token())
            .delete()
        )
        self.__config.access_token = None
        self.__config.refresh_token = None
        self.__config.session_id = None
        self.__config.account_id = None

    def refresh_token(self) -> AuthResponse:
        """refresh the access token

        Raises:
            ValueError: if refresh token is missing

        Returns:
            AuthResponse: the new credentials
        """
        if not self.__config.refresh_token:
            raise ValueError("refresh token is missing")

        data = {"refresh_token": self.__config.refresh_token}

        response = (
            HttpClient(self.__config, url=_REFRESH_URL)
            .set_authorization_header(self.__config.get_token())
            .post(data)
        )

        login = response.deserialize(AuthResponse)
        self.__load_credentials(login)

        return login

    def __load_credentials(self, login: AuthResponse) -> None:
        """loads the credentials from the response to the config

        Args:
            login (AuthResponse): credentials to load
        """
        self.__config.access_token = login.access_token
        self.__config.refresh_token = login.refresh_token
        self.__config.session_id = login.session_id
        self.__config.account_id = login.account_id
