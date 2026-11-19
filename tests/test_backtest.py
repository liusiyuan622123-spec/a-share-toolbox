import pandas as pd
import pytest

from ashare_toolbox.backtest import backtest


def test_backtest_executes_signal_on_next_session_and_charges_costs():
    close = pd.Series([10.0, 11.0, 12.0])
    signal = pd.Series([1, 1, 0])

    result = backtest(close, signal, fee_rate=0.01, slippage=0.01)

    assert result["position"].tolist() == [0.0, 1.0, 1.0]
    assert result["daily_return"].tolist() == pytest.approx(
        [0.0, 0.08, 12 / 11 - 1]
    )


def test_backtest_rejects_mismatched_indexes():
    close = pd.Series([10.0, 11.0], index=[0, 1])
    signal = pd.Series([0, 1], index=[1, 2])

    with pytest.raises(ValueError, match="identical indexes"):
        backtest(close, signal)
