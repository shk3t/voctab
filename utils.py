import os
import enum


SUCCESS_THRESHOLD = 1.0
FAIL_THRESHOLD = 0.8
DEFAULT_SETSIZE = 10


def clear_console():
    os.system("clear")


class GoToMainMenuException(Exception):
    pass


class TMode(enum.Enum):
    ENtoRU = 1
    RUtoEN = 2


def argwrap(func, *args, **kwargs):
    def wrapper():
        func(*args, **kwargs)

    return wrapper


def df_to_sqlable(df):
    return list(df.to_dict(orient="index").values())
