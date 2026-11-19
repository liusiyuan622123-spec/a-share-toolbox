"""Research utilities for China A-share market data."""

from .backtest import backtest
from .indicators import ema, macd, rsi, sma
from .signals import macd_cross, moving_average_cross

__all__ = [
    "backtest",
    "ema",
    "macd",
    "macd_cross",
    "moving_average_cross",
    "rsi",
    "sma",
]
