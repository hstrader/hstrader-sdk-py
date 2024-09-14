from ..helpers import HttpClient
from ..config import Config
from ..models import Position, UpdPosition, ClsPosition
from typing import List, Union
from .urls import (
    URL_GETMYPOSITIONS,
    URL_UPDATEMYPOSITION_POSITION_ID,
    URL_CLOSEMYPOSITION_POSITION_ID,
    URL_GETMYPOSITIONSHISTORY
)


class PositionService:
    def __init__(self, config: Config):
        self.__config: Config = config

    def get_positions(self) -> List[Position]:
        """get the list of positions

        Returns:
            List[Position]: the list of positions
        """
        response = (
            HttpClient(self.__config, url=URL_GETMYPOSITIONS)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        return response.deserialize_list(Position)


    def get_position_history(self) -> List[Position]:
        """get the list of positions

        Returns:
            List[Position]: the list of positions
        """
        response = (
            HttpClient(self.__config, url=URL_GETMYPOSITIONSHISTORY)
            .set_authorization_header(self.__config.get_token())
            .get()
        )
        return response.deserialize_list(Position)
    def update_position(self, position: Union[UpdPosition, dict]) -> str:
        """update am existing position

        Args:
            position_id (int): the position id
            position (UpdPosition | dict): the new position data

        Returns:
            str: _description_
        """
        response = (
            HttpClient(
                self.__config,
                url=URL_UPDATEMYPOSITION_POSITION_ID.replace(
                    "%v", str(position.position_id)
                ),
            )
            .set_authorization_header(self.__config.get_token())
            .put(position)
        )
        return response.data

    def close_position(self, data: ClsPosition) -> str:
        response = (
            HttpClient(
                self.__config,
                url=URL_CLOSEMYPOSITION_POSITION_ID.replace(
                    "%v", str(data.position_id)
                ),
            )
            .set_authorization_header(self.__config.get_token())
            .post(data)
        )
        return response.data

