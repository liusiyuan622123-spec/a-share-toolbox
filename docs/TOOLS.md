# A 股数据与量化工具

此目录用于发现和评估公开项目，不代表对其安全性、数据准确性或投资表现的保证。接入前请自行检查维护状态、许可证、服务条款和数据授权。

## 行情数据

| 项目 | 说明 | 链接 |
| --- | --- | --- |
| AkShare | 开源财经数据接口集合，包含多类中国市场数据；接口可用性依赖上游网站 | [GitHub](https://github.com/akfamily/akshare) |
| BaoStock | 提供证券历史行情等数据查询接口，适合研究和教学 | [GitHub](https://github.com/baostock/baostock) |
| Tushare | 金融数据接口服务；部分数据或功能需注册、积分或遵守其服务条款 | [官网](https://tushare.pro/) |

## 研究与回测

| 项目 | 说明 | 链接 |
| --- | --- | --- |
| Qlib | 微软开源的量化研究平台，可用于数据处理、模型研究和策略评估 | [GitHub](https://github.com/microsoft/qlib) |
| Backtrader | Python 回测框架；使用前确认其数据适配和交易规则是否符合 A 股需求 | [GitHub](https://github.com/mementum/backtrader) |
| vectorbt | 基于向量化计算的量化分析与回测工具 | [GitHub](https://github.com/polakowo/vectorbt) |

## 选择建议

- 先用小规模样本验证数据字段、复权方式、停牌和缺失值处理。
- 回测中显式建模佣金、印花税、滑点、涨跌停、交易单位和成交限制。
- 注意幸存者偏差、未来函数、数据修订与样本外验证。
- 不要把 API 密钥、账户凭证或个人数据提交到仓库。
