from __future__ import annotations

import numpy as np
import pandas as pd


def backtest(
    close: pd.Series,
    signal: pd.Series,
    fee_rate: float = 0.0003,
    slippage: float = 0.0005,
) -> pd.DataFrame:
    """Backtest a long-only 0/1 signal with next-session execution.

    ``signal`` is shifted by one row before applying daily close-to-close
    returns, preventing same-day close information from earning that day's
    return. Costs are charged on absolute position changes.
    """
    if not isinstance(close, pd.Series) or not isinstance(signal, pd.Series):
        raise TypeError("close and signal must be pandas Series")
    if not close.index.equals(signal.index):
        raise ValueError("close and signal must have identical indexes")
    if not np.isfinite(fee_rate) or not np.isfinite(slippage):
        raise ValueError("fee_rate and slippage must be finite")
    if fee_rate < 0 or slippage < 0:
        raise ValueError("fee_rate and slippage must be non-negative")
    if close.empty:
        raise ValueError("close and signal must not be empty")
    if close.isna().any() or signal.isna().any():
        raise ValueError("close and signal must not contain missing values")
    if not close.map(np.isfinite).all() or (close <= 0).any():
        raise ValueError("close values must be finite and positive")
    if not signal.isin([0, 1, False, True]).all():
        raise ValueError("signal values must be 0 or 1")

    position = signal.astype(float).shift(1, fill_value=0.0)
    turnover = position.diff().abs()
    turnover.iloc[0] = position.iloc[0]
    costs = turnover * (fee_rate + slippage)
    daily_returns = close.pct_change().fillna(0.0)
    strategy_returns = position * daily_returns - costs

    return pd.DataFrame(
        {
            "position": position,
            "turnover": turnover,
            "cost": costs,
            "daily_return": strategy_returns,
            "equity": (1 + strategy_returns).cumprod(),
        },
        index=close.index,
    )
