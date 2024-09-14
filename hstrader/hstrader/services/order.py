from ..helpers import HttpClient
from ..config import Config
from ..models import *
from typing import List
from .urls import (
    _URL_UPDATEMYORDER_ORDER_ID,
    _URL_CREATEMYORDER,
    _URL_CANCELMYORDER_ORDER_ID,
    _URL_GETMYORDERS,
    _URL_GETMYORDERSHistory
)


class OrderService:
    def __init__(self, config: Config):
        self.__config: Config = config

    def create_order(self, order: Union[CrtOrder, dict]) -> str:
        """send an order to the server

        Args:
            order (CrtOrder | dict): the order to send

        Returns:
            str: response from the server
        """
        response = (
            HttpClient(self.__config, url=_URL_CREATEMYORDER)
            .set_authorization_header(self.__config.get_token())
            .post(order)
        )
        return response

    def cancel_order(self, order_id: int) -> None:
        """cancel an order

        Args:
            order_id (int): the order id
        """
        (
            HttpClient(
                self.__config,
                url=_URL_CANCELMYORDER_ORDER_ID.replace("%v", str(order_id)),
            )
            .set_authorization_header(self.__config.get_token())
            .post()
        )

    def update_order(self, order: Union[UpdOrder, dict]) -> str:
        """update an existing order

        Args:
            order_id (int): the order id
            order (UpdOrder | dict): the new order data

        Returns:
            str: response from the server
        """
        response = (
            HttpClient(
                self.__config,
                url=_URL_UPDATEMYORDER_ORDER_ID.replace(
                    "%v", str(order.order_id)),
            )
            .set_authorization_header(self.__config.get_token())
            .put(order)
        )
        return response.data

    def get_orders(self) -> List[Order]:
        """get the list of orders of the account

        Returns:
            List[Order]: list of orders of the account
        """
        response = (
            HttpClient(self.__config, url=_URL_GETMYORDERS)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        return response.deserialize_list(Order)
    
    def get_orders_history(self) -> List[Order]:
        """get the list of orders of the account

        Returns:
            List[Order]: list of orders of the account
        """
        response = (
            HttpClient(self.__config, url=_URL_GETMYORDERSHistory)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        return response.deserialize_list(Order)
