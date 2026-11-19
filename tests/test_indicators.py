import pandas as pd
import pytest

from ashare_toolbox.indicators import macd, rsi, sma
from ashare_toolbox.risk import annualized_volatility, max_drawdown
from ashare_toolbox.screeners import above_sma, relative_volume
from ashare_toolbox.signals import macd_cross


def test_sma_and_rsi_handle_warmup_and_flat_prices():
    close = pd.Series([10.0, 10.0, 10.0, 10.0])

    assert sma(close, 3).iloc[:2].isna().all()
    assert rsi(close, 2).iloc[:2].isna().all()
    assert rsi(close, 2).iloc[2:].tolist() == [50.0, 50.0]


def test_macd_and_screeners_return_aligned_series():
    close = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    volume = pd.Series([100.0, 100.0, 100.0, 100.0, 200.0])

    values = macd(close, fast=2, slow=3, signal=2)

    assert list(values.columns) == ["macd", "signal", "histogram"]
    assert len(macd_cross(close, fast=2, slow=3, signal=2)) == len(close)
    assert above_sma(close, window=2).tolist() == [False, True, True, True, True]
    assert relative_volume(volume, window=2).iloc[-1] == 2.0


def test_risk_metrics_measure_drawdown_and_sample_volatility():
    equity = pd.Series([1.0, 1.2, 0.9, 1.1])
    returns = pd.Series([0.01, -0.02, 0.03])

    assert max_drawdown(equity) == pytest.approx(-0.25)
    assert annualized_volatility(returns, periods_per_year=1) == pytest.approx(
        returns.std(ddof=1)
    )
