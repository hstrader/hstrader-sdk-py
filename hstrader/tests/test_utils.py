from hstrader.services.utils import convert_time_to_int
import datetime as dt
import time


def test_convert_time_to_int_int():
    assert convert_time_to_int(1609452000) == 1609452000


def test_convert_time_to_int_float():
    assert convert_time_to_int(1609452000.0) == 1609452000


def test_convert_time_to_int_str():
    assert convert_time_to_int("2021-01-01") == 1609452000


def test_convert_time_to_int_datetime():
    assert convert_time_to_int(dt.datetime(2021, 1, 1)) == 1609452000


def test_convert_time_to_int_time():
    assert convert_time_to_int(time.time()) == int(time.time())
