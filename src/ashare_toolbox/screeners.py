from __future__ import annotations

import pandas as pd


def above_sma(close: pd.Series, window: int = 20) -> pd.Series:
    """Mark dates where close is above its simple moving average."""
    if not isinstance(close, pd.Series):
        raise TypeError("close must be a pandas Series")
    if window < 1:
        raise ValueError("window must be positive")
    average = close.rolling(window=window, min_periods=window).mean()
    return (close > average).fillna(False).rename("above_sma")


def relative_volume(volume: pd.Series, window: int = 20) -> pd.Series:
    """Compare each day's volume to the preceding ``window`` sessions.

    The baseline excludes the current session to avoid including the value
    being measured in its own comparison.
    """
    if not isinstance(volume, pd.Series):
        raise TypeError("volume must be a pandas Series")
    if window < 1:
        raise ValueError("window must be positive")
    baseline = volume.shift(1).rolling(window=window, min_periods=window).mean()
    return (volume / baseline).rename("relative_volume")
