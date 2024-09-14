import asyncio

import websockets
from ..config import Config

from typing import Callable
import inspect


from .user_agent import __USER_AGENT__


class WebSocketClient:
    def __init__(self, config: Config, url: str) -> None:
        """Create a new instance of the WebSocketService

        Args:
            config (Config): the configuration object to be used for the service
        """

        self.__config: Config = config
        self.__connection = None
        self.__loop = asyncio.get_event_loop()
        self.__on_connect = None
        self.__on_disconnect = None
        self.__on_message = None
        self.__url = url

    async def start_async(self):
        """Start the websocket connection asynchronously, this method should be called using asyncio

        Raises:
            ValueError: if the connection is already established
        """

        authorization_header = (
            "Authorization", f"Bearer {self.__config.get_token()}")
        user_agent_header = ("User-Agent", __USER_AGENT__)

        if self.__config.is_connected:
            raise ValueError("Already connected to the server")

        async with websockets.connect(
            self.__url, extra_headers=[authorization_header, user_agent_header]
        ) as websocket:
            self.__connection = websocket
            await self.__handle_message(websocket)

    def stop(self):
        """Stop the websocket connection"""
        if self.__connection is None or not self.__config.is_connected:
            raise ValueError(
                "You can't stop a connection without starting it first")
        self._run(self.__connection.close)

    def start(self):
        """Start the websocket connection, this function will block the current thread,
        if you want to start the connection asynchronously use start_async instead
        """
        self.__loop.run_until_complete(self.start_async())

    def _send_message(self, message: str):
        """Send a message to the server, only for debugging purposes

        Args:
            message (str): _description_
        """
        self.__loop.create_task(self.__connection.send(message))

    async def __handle_message(self, websocket: websockets.connect):
        """Handle the messages received from the server

        Args:
            websocket (websockets.connection.Connection): the websocket connection
            path (str): the path of the websocket connection
        """

        try:

            self.__run_on_connect()

            async for message in websocket:
                if message is websockets.protocol.State.CLOSED:
                    break
                self.__run_on_message(message)

            self.__run_on_disconnect()
        except Exception as e:
            raise e
            # self.__on_disconnect()
            # self.__loop.stop()

    def _set_on_connect(self, handler: Callable):
        """Set the handler for the connect event

        Args:
            handler (Callable): the handler to be called when the connect event is received
        """
        if not callable(handler):
            raise ValueError("Handler must be a callable")
        if handler.__code__.co_argcount != 0:
            raise ValueError(
                f"Handlerof for Event.CONNECT must not take any arguments, got {handler.__code__.co_argcount} arguments"
            )
        self.__on_connect = handler

    def _set_on_disconnect(self, handler: Callable):
        """Set the handler for the disconnect event

        Args:
            handler (Callable): the handler to be called when the disconnect event is received
        """
        if not callable(handler):
            raise ValueError("Handler must be a callable")
        if handler.__code__.co_argcount != 0:
            raise ValueError(
                f"Handler for Event.DISCONNECT must not take any arguments, got {handler.__code__.co_argcount} arguments"
            )
        self.__on_disconnect = handler

    def _set_on_message(self, handler: Callable):
        """Set the handler for the message event

        Args:
            handler (Callable): the handler to be called when a message is received
        """
        if not callable(handler):
            raise ValueError("Handler must be a callable")
        if handler.__code__.co_argcount != 2:
            raise ValueError(
                "Handler must take two arguments, self and message")
        self.__on_message = handler

    def __run_on_connect(self):
        """Run the on_connect handler if it's set
        """

        self.__config.is_connected = True
        if self.__on_connect:
            self._run(self.__on_connect)

    def __run_on_disconnect(self):
        """Run the on_disconnect handler if it's set
        """

        self.__config.is_connected = False
        if self.__on_disconnect:
            self._run(self.__on_disconnect)

    def __run_on_message(self, message: str):
        """Run the on_message handler if it's set

        Args:
            message (str): the message received from the server
        """

        if self.__on_message:
            self._run(self.__on_message, message)

    def _create_task(self, f: Callable, *args, **kwargs):
        """Create a new task using the event loop

        Args:
            f (Callable): the function to run

        """
        self.__loop.create_task(f(*args, **kwargs))

    def _run(self, f: Callable, *args, **kwargs) -> any:
        """Run a function, if the function is a coroutine function, it will be run using the event loop

        Args:
            f (Callable): the function to run, whether it's a coroutine function or a normal function

        Returns:
            _type_: whatever the function returns
        """
        if not callable(f):
            raise ValueError("f must be a callable")

        if inspect.iscoroutinefunction(f):
            return self.__loop.create_task(f(*args, **kwargs))
        else:
            return f(*args, **kwargs)
