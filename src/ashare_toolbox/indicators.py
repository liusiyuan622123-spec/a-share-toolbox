from __future__ import annotations

import pandas as pd


def _validate_series(series: pd.Series, name: str) -> None:
    if not isinstance(series, pd.Series):
        raise TypeError(f"{name} must be a pandas Series")


def sma(close: pd.Series, window: int) -> pd.Series:
    """Simple moving average with a full-window warm-up period."""
    _validate_series(close, "close")
    if window < 1:
        raise ValueError("window must be positive")
    return close.rolling(window=window, min_periods=window).mean().rename("sma")


def ema(close: pd.Series, span: int) -> pd.Series:
    """Exponential moving average with a full-span warm-up period."""
    _validate_series(close, "close")
    if span < 1:
        raise ValueError("span must be positive")
    return close.ewm(span=span, min_periods=span, adjust=False).mean().rename("ema")


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Wilder-style relative strength index on a close-price series."""
    _validate_series(close, "close")
    if period < 1:
        raise ValueError("period must be positive")

    changes = close.diff()
    gains = changes.clip(lower=0)
    losses = -changes.clip(upper=0)
    average_gain = gains.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False,
    ).mean()
    average_loss = losses.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False,
    ).mean()
    relative_strength = average_gain / average_loss
    result = 100 - 100 / (1 + relative_strength)
    result = result.mask((average_loss == 0) & (average_gain > 0), 100)
    result = result.mask((average_gain == 0) & (average_loss == 0), 50)
    return result.rename("rsi")


def macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """Return MACD, signal, and histogram series."""
    _validate_series(close, "close")
    if min(fast, slow, signal) < 1:
        raise ValueError("MACD windows must be positive")
    if fast >= slow:
        raise ValueError("fast window must be smaller than slow window")

    line = close.ewm(span=fast, min_periods=fast, adjust=False).mean() - close.ewm(
        span=slow,
        min_periods=slow,
        adjust=False,
    ).mean()
    signal_line = line.ewm(
        span=signal,
        min_periods=signal,
        adjust=False,
    ).mean()
    return pd.DataFrame(
        {
            "macd": line,
            "signal": signal_line,
            "histogram": line - signal_line,
        },
        index=close.index,
    )
