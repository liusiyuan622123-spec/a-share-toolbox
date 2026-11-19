# A 股工具箱

面向中国 A 股的轻量研究工具集合：包含可运行的行情数据适配器、选股信号与简易回测示例，也整理常用的开源数据和量化项目。

> **风险提示：**本项目仅用于学习和研究，不构成投资建议，也不提供自动下单功能。行情数据可能延迟、缺失或有调整；回测结果不代表未来表现。使用前请核对数据授权、交易规则、复权方式、停牌和涨跌停等因素。

## 快速开始

需要 Python 3.10 或更高版本。

```bash
python -m pip install -e ".[market,dev]"
pytest
```

使用 AkShare 获取日线并计算均线交叉信号：

```python
from ashare_toolbox.providers.akshare import fetch_daily
from ashare_toolbox.signals import moving_average_cross

prices = fetch_daily("600000", start_date="20240101", end_date="20241231")
prices["signal"] = moving_average_cross(prices["Close"], fast=5, slow=20)
print(prices.tail())
```

信号表示当日收盘后产生的持仓意向；回测时必须延后一天执行，避免未来数据泄漏：

```python
from ashare_toolbox.backtest import backtest

result = backtest(prices["Close"], prices["signal"])
print(result.tail())
```

## 内置模块

- **AkShare 日线适配器**：拉取沪深京 A 股日线数据并统一列名。
- **技术指标**：SMA、EMA、RSI、MACD。
- **信号与筛选**：均线/MACD 交叉信号、收盘价相对均线位置、相对成交量。
- **简易回测**：延后一日执行信号，计入换手成本；不包含完整的交易所撮合、税费规则或组合管理。
- **风险统计**：最大回撤和年化波动率。

## 工具与项目目录

见 [`docs/TOOLS.md`](docs/TOOLS.md)。收录数据接口和量化研究框架；它们不是都能直接安装为交易软件插件，具体能力、许可和数据条款请以各项目官方说明为准。

## 贡献

欢迎提交数据源适配器、信号插件和测试。请说明数据来源及许可、交易日历/复权处理方式，并避免将历史回测描述为收益承诺。
