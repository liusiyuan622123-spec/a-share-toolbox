"""Research utilities for China A-share market data."""

from .backtest import backtest
from .signals import moving_average_cross

__all__ = ["backtest", "moving_average_cross"]
