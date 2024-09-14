from . import client, EURUSD_ID
from hstrader import HsTrader
import time
import datetime as dt
from datetime import timedelta


def test_get_market_history(client: HsTrader, EURUSD_ID: int):
    history = client.get_market_history(EURUSD_ID, count_back=10)
    assert len(history) > 0
    assert history[0].time is not None
    assert history[0].open is not None
    assert history[0].high is not None
    assert history[0].low is not None
    assert history[0].close is not None
    assert history[0].volume is not None


def test_get_market_history_from_to_int(client: HsTrader, EURUSD_ID: int):
    history = client.get_market_history(EURUSD_ID, 0, time.time(), count_back=10)
    assert len(history) > 0
    assert history[0].time is not None
    assert history[0].open is not None
    assert history[0].high is not None
    assert history[0].low is not None
    assert history[0].close is not None
    assert history[0].volume is not None


def test_get_market_history_from_to_str(client: HsTrader, EURUSD_ID: int):
    history = client.get_market_history(
        EURUSD_ID,
        (dt.datetime.now() - timedelta(hours=1)).isoformat(),
        dt.datetime.now().isoformat(),
        count_back=10,
    )
    assert len(history) > 0
    assert history[0].time is not None
    assert history[0].open is not None
    assert history[0].high is not None
    assert history[0].low is not None
    assert history[0].close is not None
    assert history[0].volume is not None


def test_get_market_history_from_to_datetime(client: HsTrader, EURUSD_ID: int):
    history = client.get_market_history(
        EURUSD_ID,
        dt.datetime.now() - timedelta(hours=1),
        dt.datetime.now(),
        count_back=10,
    )
    assert len(history) > 0
    assert history[0].time is not None
    assert history[0].open is not None
    assert history[0].high is not None
    assert history[0].low is not None
    assert history[0].close is not None
    assert history[0].volume is not None
