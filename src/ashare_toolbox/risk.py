from __future__ import annotations

import math

import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    """Return the minimum peak-to-trough drawdown as a negative fraction."""
    if not isinstance(equity, pd.Series):
        raise TypeError("equity must be a pandas Series")
    if equity.empty:
        raise ValueError("equity must not be empty")
    if equity.isna().any() or (equity <= 0).any():
        raise ValueError("equity values must be positive and non-missing")
    return float((equity / equity.cummax() - 1).min())


def annualized_volatility(
    daily_returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """Annualize sample standard deviation of daily returns."""
    if not isinstance(daily_returns, pd.Series):
        raise TypeError("daily_returns must be a pandas Series")
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be positive")
    returns = daily_returns.dropna()
    if len(returns) < 2:
        raise ValueError("at least two non-missing returns are required")
    if not returns.map(math.isfinite).all():
        raise ValueError("daily_returns must be finite")
    return float(returns.std(ddof=1) * math.sqrt(periods_per_year))
