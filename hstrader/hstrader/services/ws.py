import json
from ..config import Config
from ..helpers import WebSocketClient
from ..models import *
from typing import Callable, Union
from .utils import *
import logging


class _WS_Event(Enum):
    START_MARKET_FEED = "start_market_feed"
    STOP_MARKET_FEED = "stop_market_feed"
    BAD_REQUEST = "bad_request"
    ORDER_CREATE = "order_create"
    ORDER_UPDATE = "order_update"
    ORDER_CANCEL = "order_cancel"
    POSITION_CREATE = "position_create"
    POSITION_CLOSE = "position_close"
    POSITION_UPDATE = "position_update"
    POSITION_PROFIT_LOSS = "position_pl"
    DEAL_CREATE = "deal_create"
    DEAL_UPDATE = "deal_update"
    WATCHLIST_CREATE = "watchlist_create"
    WATCHLIST_UPDATE = "watchlist_update"
    WATCHLIST_DELETE = "watchlist_delete"
    SYMBOL_UPDATE = "symbol_update"
    SYMBOL_CREATE = "symbol_create"


class WebSocketService:
    def __init__(self, config: Config):
        """Create a new instance of the WebSocketService

        Args:
            config (Config): the configuration object to be used for the service
        """

        self.__message_handlers = {
            Event.ERROR.value: self.__bad_request,
        }
        self.__config: Config = config

        self.__client = WebSocketClient(config, self.__get_url())
        self.__client._set_on_message(self.__on_message)
        self.__client._set_on_connect(self.__get_on_connect_callback())
        self.__client._set_on_disconnect(self.__get_on_disconnect_callback())

    def subscribe(self, event: Union[Event, str] = None):
        """Decorator to register a handler for a specific event

        Args:
            event (Event): the event to register the handler for
        """

        def decorator(func: Callable):
            """decorator to register a handler for a specific event

            Args:
                func (Callable): a callable function that will be called when the event is received

            """
            self.register_handler(event, func)
            return func

        return decorator

    def register_handler(self, event: Union[Event, str], handler: Callable):
        """Add a handler for a specific event

        Args:
            handler (Callable): the handler function to be called when the event is received
            event (Event): the event to be handled
        """

        if event is None or handler is None:
            raise ValueError("Event and handler must be provided")

        if not isinstance(event, Event) and not isinstance(event, str):
            raise ValueError("Event must be an instance of Event Enum or a string")

        if not callable(handler):
            return

        if isinstance(event, str):
            event = event.lower()
            # check if event is valid
            if event == "error":
                event = "bad_request"
            if event in ["profit_loss", "pl", "profit", "loss", "position_profit_loss"]:
                event = "position_pl"

            elif event not in [e.value for e in Event]:
                raise ValueError(
                    f'Invalid event "{event}", must be one of [ {", ".join([e.value for e in Event])}, error]'
                )
            event = Event(event)

        # if event == Event.CONNECT:
        #     self.__client._set_on_connect(handler)
        #     return
        # elif event == Event.DISCONNECT:
        #     self.__client._set_on_disconnect(handler)
        #     return
        if event in [Event.CONNECT, Event.DISCONNECT]:
            if handler.__code__.co_argcount != 0:
                raise ValueError(
                    f"Handler for {event} must not take any arguments, got {handler.__code__.co_argcount} arguments"
                )

        elif event in [Event.MARKET, Event.SUMMARY, Event.ERROR, Event.POSITION_PL]:
            if handler.__code__.co_argcount != 1:
                raise ValueError(
                    f"Handler for {event} must have exactly one argument, got {handler.__code__.co_argcount} arguments"
                )
        else:
            if handler.__code__.co_argcount != 2:
                raise ValueError(
                    f"Handler for {event} must have exactly two arguments, got {handler.__code__.co_argcount} arguments"
                )

        self.__message_handlers[event.value] = handler

    def start_market_feed(self):
        """Start the market feed, this will start receiving ticks from the server, called only after the connection is established"""
        self.__send_event(_WS_Event.START_MARKET_FEED, {})

    def stop_market_feed(self):
        """Stop the market feed, this will stop receiving ticks from the server, called only after the connection is established"""
        self.__send_event(_WS_Event.STOP_MARKET_FEED, {})

    def create_order(self, order: CrtOrder):
        """Send a new order to the server, called only after the connection is established

        Args:
            order (CrtOrder): Order to send to the server
        """
        self.__send_event(_WS_Event.ORDER_CREATE, order)

    def update_order(self, order: UpdOrder):
        """Update an existing order, called only after the connection is established

        Args:
            order (UpdOrder): Data to update the order
        """
        self.__send_event(_WS_Event.ORDER_UPDATE, order)

    def cancel_order(self, id: int):
        """Cancel an existing order, called only after the connection is established

        Args:
            order (CancelOrder): the order to cancel
        """
        order = CnlOrder(order_id=id)
        self.__send_event(_WS_Event.ORDER_CANCEL, order)

    def close_position(self, position: ClsPosition):
        """Close an existing position, called only after the connection is established

        Args:
            position (ClsPosition): the position to close
        """
        self.__send_event(_WS_Event.POSITION_CLOSE, position)

    def update_position(self, position: UpdPosition):
        """Update an existing position, called only after the connection is established

        Args:
            position (UptPosition): the position to update
        """
        self.__send_event(_WS_Event.POSITION_UPDATE, position)

    async def start_async(self):
        """Start the websocket connection asynchronously"""
        try:
            return await self.__client.start_async()
        except Exception:
            raise ConnectionAbortedError(
                "The connection was closed unexpectedly: " + e.__str__()
            ) from None

    def start(self):
        """Start the websocket connection"""
        try:
            self.__client.start()
        except Exception as e:
            raise ConnectionAbortedError(
                "The connection was closed unexpectedly: " + e.__str__()
            ) from None

    def stop(self):
        """Stop the websocket connection"""
        return self.__client.stop()

    async def __on_message(self, message: str):
        """Handle the messages received from the server

        Args:
            websocket (websockets.connection.Connection): the websocket connection
            path (str): the path of the websocket connection
        """

        try:

            # Get the type and status of the message (status is None if the message is not an order or position or deal)
            typ, status = self.__get_message_type(message)
            if typ is None:
                return

            # Get the handler for the message type
            handler = self.__get_handler(typ)
            # An edge case where the pl event received from the server is not handled
            if (
                handler is None
                and typ == Event.SUMMARY
                and self.__get_handler(Event.POSITION_PL) is not None
            ):
                handler = self.__get_handler(Event.POSITION_PL)
            # If the handler is found, parse the payload and run the handler
            if handler:
                if typ == Event.MARKET:
                    self.__handle_market(self.__unpack_payload(typ, message))
                elif typ == Event.SUMMARY:
                    summary, pl = self.__unpack_payload(typ, message)
                    self.__handle_summary(summary, pl)
                else:
                    self.__run_callback(
                        handler, self.__unpack_payload(typ, message), status
                    )

        except Exception as e:
            raise Exception(
                f"An error occurred while processing the message { message.__str__()}"
            ) from e

    def __send_event(self, event: Event, payload: Union[BaseModel, dict]):
        """Send an event to the server

        Args:
            event (Event): the event to send
            payload (BaseModel | dict): the payload to send with the event

        Raises:
            ValueError: if the connection is not established
        """

        if not self.__config.is_connected:
            raise ValueError("Not connected to the server")
        try:
            pload = payload
            if isinstance(payload, BaseModel):
                pload = payload.model_dump()

            data = WsMessage(type=event.value, payload=pload).model_dump()
            marshalled = json.dumps(data)

            self.__client._send_message(marshalled)
        except Exception:
            pass

    def __run_callback(self, f: Callable, data: any, status: Status):
        """Run a callback function

        Args:
            f (Callable): the function to run
            data (any): the data coming from the websocket to pass to the function
            status (Status): the status of the event, whether it was created, updated or deleted

        Returns:
            _type_: whatever the function returns
        """
        if status is None:
            return self.__client._run(f, data)
        else:
            return self.__client._run(f, data, status)

    def __unpack_payload(self, event: Event, message: Union[str, bytes]) -> any:
        """Unpack the payload received from the server, this will deserialize the message to the appropriate model


        Args:
            event (Event): the event of the message
            message (str | bytes): the message received from the server

        Returns:
            any: the unpacked payload
        """

        try:

            if event == Event.MARKET:
                return deserialize_tick(message)
            elif event == Event.SUMMARY:
                return deserialize_summary(message)
            else:
                model = events_deserializer.get(event)
                if model:
                    return deserialize_model(model, message)
                return None
        except Exception as e:
            pass
        return None

    def __get_message_type(
        self, message: Union[str, bytes]
    ) -> (Event, Union[Status, None]):
        """return the message type and status if any where:
        - message: the message received from the server

        Args:
            self (_type_): _description_
            message (_type_): _description_

        Returns:
            _Event_: the event type whether it was a market, summary, order or any other event
            _Status_: the status of the event whether it was created, updated or deleted
        """
        try:

            if isinstance(message, bytes):
                return Event.MARKET, None
            if isinstance(message, str):
                if message.startswith(Event.SUMMARY.value):
                    return Event.SUMMARY, None
                else:
                    unmarshalled = json.loads(message)
                    typ = unmarshalled.get("type")

                    if typ == Event.ERROR.value:
                        return Event.ERROR, None

                    splitted = typ.split("_")
                    return Event(splitted[0]), Status(splitted[1])

        except Exception as e:
            logging.debug(e)
            return None, None

    def __get_url(self) -> str:
        """Get the websocket url to connect to

        Raises:
            ValueError: if the session id is not set

        Returns:
            str: the websocket url to connect to
        """
        if self.__config is None or self.__config.session_id is None:
            raise ValueError(
                "You need to login first to connect to the websocket service."
            )

        return f"wss://{self.__config.get_url()}/ws/v1?session_id={self.__config.session_id}"

    def __bad_request(self, message: str):
        """Handle a bad request received from the server

        Args:
            message (str): the message received from the server
        """
        if not self.__config.disable_logging:
            logging.error(f"Bad request: {message}")

    def __handle_market(self, tick: Tick):
        """Handle a market event received from the server, this will add the spread to the bid and ask prices

        Args:
            tick (Tick): the tick received from the server
        """

        symbol = self.__config.get_symbol(tick.symbol_id)
        if symbol is None:
            return
        bid_spread, ask_spread = calculate_spread(symbol)
        tick.bid = truncate_float(tick.bid + bid_spread, symbol.digits)
        if symbol.spread is not None:
            tick.ask = truncate_float(tick.bid + symbol.spread, symbol.digits)
        else:
            tick.ask = truncate_float(tick.ask + ask_spread, symbol.digits)

        self.__run_callback(self.__get_handler(Event.MARKET), tick, None)

    def __handle_summary(self, summary: Summary, pl: List[PositionPL]):
        """Handle a summary event received from the server

        Args:
            summary (Summary): the summary received from the server
        """

        summary_handler = self.__get_handler(Event.SUMMARY)
        if summary_handler:
            self.__run_callback(summary_handler, summary, None)

        pl_handler = self.__get_handler(Event.POSITION_PL)
        if pl_handler:
            for pl in pl:
                self.__run_callback(pl_handler, pl, None)

    def __get_handler(self, event: Union[Event, str]) -> Callable:
        """Get the callback function for a specific event

        Args:
            event (Event): the event to get the callback for
        """
        if isinstance(event, str):
            return self.__message_handlers.get(event)
        return self.__message_handlers.get(event.value)

    def __get_on_connect_callback(self):
        """Handle the connection event"""

        def on_connect():
            if Event.MARKET.value in self.__message_handlers:
                self.start_market_feed()
            handler = self.__get_handler(Event.CONNECT)
            if handler:
                self.__client._run(handler)

        return on_connect

    def __get_on_disconnect_callback(self):

        def on_disconnect():
            handler = self.__get_handler(Event.DISCONNECT)
            if handler:
                self.__client._run(handler)

        return on_disconnect
