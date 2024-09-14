from .base import BaseModel
import datetime


class HistoryTick(BaseModel):
    time: datetime.datetime = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None

    def __init__(
        self,
        time: datetime.datetime,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float,
    ):
        super().__init__(
            time=time,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume,
        )
