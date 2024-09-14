import requests
from typing import Union
from ..config import Config
from ..models import BaseResponse
from typing_extensions import Self
from pydantic import BaseModel
from typing import Callable
from .user_agent import __USER_AGENT__

http_method_to_string = {
    requests.get: "GET",
    requests.post: "POST",
    requests.put: "PUT",
    requests.patch: "PATCH",
    requests.delete: "DELETE",
}


class HttpClient:
    def __init__(self, config: Config, url: str) -> None:
        self.__config: Config = config
        self.url = "https://" + self.__config.get_url() + url
        self.headers = {"User-Agent": __USER_AGENT__}

    def set_authorization_header(self, token: str) -> Self:
        """set the authorization header

        Args:
            token (str): the token to set

        Returns:
            Self: same instance of HttpClient
        """
        return self.set_headers({"Authorization": f"Bearer {token}"})

    def set_headers(self, headers: dict) -> Self:
        """set the headers of the request

        Args:
            headers (dict): any header you want to set or override

        Returns:
            Self: same instance of HttpClient
        """
        for key, value in headers.items():
            self.headers[key] = value
        return self

    def get(self, params=None) -> Union[BaseResponse, None]:
        """perform a get request

        Returns:
            BaseResponse|None: the standard response from the server
        """
        response = self.__send_request(
            requests.get,
            url=self.url,
            headers=self.headers,
            params=params,
            timeout=self.__config.timeout,
        )

        baseResp = self.__check_response(response)

        return baseResp

    def post(self, data: Union[dict, BaseModel] = None) -> Union[BaseResponse, None]:
        """perform a post request

        Args:
            data (Union[dict, BaseModel], optional): the data to post. Defaults to None.

        Returns:
            BaseResponse|None: the standard response from the server
        """
        if isinstance(data, BaseModel):
            data = data.model_dump()
        response = self.__send_request(
            requests.post,
            url=self.url,
            json=data,
            headers=self.headers,
            timeout=self.__config.timeout,
        )

        baseResp = self.__check_response(response)
        return baseResp

    def put(self, data: Union[dict, BaseModel] = None) -> Union[BaseResponse, None]:
        """perform a put request

        Args:
            data (Union[dict, BaseModel], optional): the data to update. Defaults to None.

        Returns:
            BaseResponse|None: the standard response from the server
        """
        if isinstance(data, BaseModel):
            data = data.model_dump()

        response = self.__send_request(
            requests.put,
            url=self.url,
            json=data,
            headers=self.headers,
            timeout=self.__config.timeout,
        )

        baseResp = self.__check_response(response)
        return baseResp

    def patch(self, data: Union[dict, BaseModel] = None) -> Union[BaseResponse, None]:
        """perform a patch request

        Args:
            data (Union[dict, BaseModel], optional): the data to update. Defaults to None.

        Returns:
            BaseResponse|None: the standard response from the server
        """
        if isinstance(data, BaseModel):
            data = data.model_dump()
        response = self.__send_request(
            requests.patch,
            url=self.url,
            json=data,
            headers=self.headers,
            timeout=self.__config.timeout,
        )

        baseResp = self.__check_response(response)
        return baseResp

    def delete(self) -> None:
        """perform a delete request"""
        response = self.__send_request(
            requests.delete,
            url=self.url,
            headers=self.headers,
            timeout=self.__config.timeout,
        )

        self.__check_response(response)

        # if response.text == "":
        #     return None
        # return response.json()

    def __check_response(self, response: requests.Response) -> BaseResponse:
        """check the response from the server and raise an error if the response is not successful

        Args:
            response (requests.Response): the response from the server

        Raises:
            ValueError: if the response is not successful

        Returns:
            BaseResponse: the standard response from the server
        """
        baseResp: BaseResponse = None

        if response.status_code == 200:
            baseResp = BaseResponse(**response.json())
            return baseResp
        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            baseResp = BaseResponse(**response.json())
            if not baseResp.success:
                raise ValueError(baseResp.message) from None

        return baseResp

    def __log_request(self, method: str, url: str, headers: dict, body: dict):
        """log the sent request

        Args:
            method (str): the method of the request
            url (str): the url of the request
            headers (dict): the headers of the request
            body (dict): the body of the request
        """

    def __log_response(self, response: requests.Response):
        """log the received response

        Args:
            response (request.Response): the response from the server
        """

    # decorator to automatically print the logs for the request and response
    def __send_request(self, f: Callable, **kwargs) -> requests.Response:
        """send the request and log the request and response

        Args:
            f (Callable): the function to send the request

        Returns:
            requests.Response: the response from the server
        """
        url = kwargs.get("url")
        headers = kwargs.get("headers")
        body = kwargs.get("json")
        method = self.__get_method(f)
        self.__log_request(method, url, headers, body)
        response = f(**kwargs)
        self.__log_response(response)
        return response

    def __get_method(self, method: Callable) -> str:
        """get the method of the request

        Args:
            method (Callable): the method of the request

        Returns:
            str: the method of the request
        """

        return http_method_to_string.get(method)
