import pandas as pd
import pytest

from ashare_toolbox.signals import moving_average_cross


def test_moving_average_cross_uses_only_available_history():
    close = pd.Series([5, 4, 3, 4, 6], dtype=float)

    signal = moving_average_cross(close, fast=2, slow=3)

    assert signal.tolist() == [0, 0, 0, 0, 1]


@pytest.mark.parametrize(
    ("fast", "slow"),
    [(0, 3), (2, 0), (3, 3), (4, 3)],
)
def test_moving_average_cross_rejects_invalid_windows(fast, slow):
    with pytest.raises(ValueError):
        moving_average_cross(pd.Series([1, 2, 3]), fast=fast, slow=slow)
