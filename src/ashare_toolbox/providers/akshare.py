from __future__ import annotations

import re

import pandas as pd


def fetch_daily(
    symbol: str,
    start_date: str,
    end_date: str,
    adjust: str = "qfq",
) -> pd.DataFrame:
    """Fetch daily A-share bars from AkShare with normalized English columns.

    Dates must be ``YYYYMMDD``. AkShare is an optional dependency and its
    upstream data availability is outside this package's control.
    """
    if not re.fullmatch(r"\d{6}", symbol):
        raise ValueError("symbol must be a six-digit A-share code")
    for label, value in (("start_date", start_date), ("end_date", end_date)):
        if not re.fullmatch(r"\d{8}", value):
            raise ValueError(f"{label} must use YYYYMMDD format")
        try:
            pd.to_datetime(value, format="%Y%m%d", errors="raise")
        except ValueError as exc:
            raise ValueError(f"{label} is not a valid date") from exc
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")
    if adjust not in {"", "qfq", "hfq"}:
        raise ValueError("adjust must be '', 'qfq', or 'hfq'")

    try:
        import akshare as ak
    except ImportError as exc:
        raise ImportError(
            "AkShare is required for this provider; install with "
            '`python -m pip install -e ".[market]"`'
        ) from exc

    raw = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )
    columns = {
        "日期": "Date",
        "开盘": "Open",
        "收盘": "Close",
        "最高": "High",
        "最低": "Low",
        "成交量": "Volume",
    }
    missing = set(columns).difference(raw.columns)
    if missing:
        raise ValueError(f"AkShare response is missing columns: {sorted(missing)}")
    result = raw.loc[:, list(columns)].rename(columns=columns)
    result["Date"] = pd.to_datetime(result["Date"], errors="raise")
    for column in ("Open", "High", "Low", "Close", "Volume"):
        result[column] = pd.to_numeric(result[column], errors="raise")
    return result.sort_values("Date").reset_index(drop=True)
