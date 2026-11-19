from __future__ import annotations

import pandas as pd

from .indicators import macd


def moving_average_cross(
    close: pd.Series,
    fast: int = 5,
    slow: int = 20,
) -> pd.Series:
    """Return a 0/1 long-only position intention from a moving-average cross.

    The value at each date uses that date's closing price and must therefore
    not be executed until the next trading session.
    """
    if fast < 1 or slow < 1:
        raise ValueError("fast and slow windows must be positive")
    if fast >= slow:
        raise ValueError("fast window must be smaller than slow window")
    if not isinstance(close, pd.Series):
        raise TypeError("close must be a pandas Series")

    fast_ma = close.rolling(window=fast, min_periods=fast).mean()
    slow_ma = close.rolling(window=slow, min_periods=slow).mean()
    return (fast_ma > slow_ma).fillna(False).astype("int8").rename("signal")


def macd_cross(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.Series:
    """Return a 0/1 long-only position intention from a MACD cross."""
    macd_values = macd(close, fast=fast, slow=slow, signal=signal)
    return (macd_values["macd"] > macd_values["signal"]).fillna(False).astype(
        "int8"
    ).rename("signal")
