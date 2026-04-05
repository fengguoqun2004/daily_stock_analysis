<div align="center">

# 📈 股票智能分析系统

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)

<p>
  <a href="https://trendshift.io/repositories/18527" target="_blank"><img src="https://trendshift.io/api/badge/repositories/18527" alt="ZhuLinsen%2Fdaily_stock_analysis | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
  <a href="https://hellogithub.com/repository/ZhuLinsen/daily_stock_analysis" target="_blank"><img src="https://api.hellogithub.com/v1/widgets/recommend.svg?rid=6daa16e405ce46ed97b4a57706aeb29f&claim_uid=pfiJMqhR9uvDGlT&theme=neutral" alt="Featured｜HelloGitHub" style="width: 250px; height: 54px;" width="250" height="54" /></a>
</p>

> 🤖 基于 AI 大模型的 A股 / 港股 / 美股自选股智能分析系统，每日自动分析并推送「决策仪表盘」到企业微信 / 飞书 / Telegram / Discord / Slack / 邮箱

[**功能特性**](#-功能特性) · [**快速开始**](#-快速开始) · [**运行与部署**](#-运行与部署) · [**推送效果**](#-推送效果) · [**文档导航**](#-文档导航) · [**更新日志**](docs/CHANGELOG.md)

简体中文 | [English](docs/README_EN.md) | [繁體中文](docs/README_CHT.md)

</div>

## 💖 赞助商 (Sponsors)

<div align="center">
  <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank">
    <img src="./sources/serpapi_banner_zh.png" alt="轻松抓取搜索引擎上的实时金融新闻数据 - SerpApi" height="160">
  </a>
</div>
<br>

## ✨ 功能特性

| 模块 | 功能 | 说明 |
|------|------|------|
| AI | 决策仪表盘 | 一句话核心结论 + 精确买卖点位 + 操作检查清单 |
| 分析 | 多维度分析 | 技术面 + 筹码分布 + 舆情情报 + 实时行情 |
| 市场 | 全球市场 | 支持 A股、港股、美股及美股指数 |
| 策略 | 市场策略系统 | 内置 A股「三段式复盘策略」与美股「Regime Strategy」 |
| Web / Desktop | 工作台 | Web 管理界面支持配置管理、任务监控、手动分析；可扩展桌面端 |
| 导入 / 搜索 | 智能补全与导入 | 支持代码 / 名称 / 拼音 / 别名联想，以及图片、CSV/Excel、剪贴板导入 |
| 回测 | AI 回测验证 | 自动评估历史分析准确率，支持次日验证 / 1 日窗口视图 |
| Agent 问股 | 策略对话 | 多轮策略问答，支持 Web / Bot / API 全链路 |
| 推送 | 多渠道通知 | 企业微信、飞书、Telegram、Discord、Slack、钉钉、邮件、Pushover |
| 自动化 | 定时运行 | GitHub Actions 定时执行，无需服务器 |

> 更细的模块说明、页面交互、专题配置与排障说明已下沉到 [docs/INDEX.md](docs/INDEX.md) 对应文档，README 仅保留高频入口。

### 技术栈与数据来源

| 类型 | 支持 |
|------|------|
| AI 模型 | [AIHubMix](https://aihubmix.com/?aff=CfMq)、Gemini、OpenAI 兼容、DeepSeek、通义千问、Claude、Ollama 等 |
| 行情数据 | AkShare、Tushare、Pytdx、Baostock、YFinance、[Longbridge](https://open.longbridge.com/) |
| 新闻搜索 | Tavily、SerpAPI、Bocha、Brave、MiniMax |
| 社交舆情 | [Stock Sentiment API](https://api.adanos.org/docs)（可选，仅美股） |

> **长桥优先策略（仅美/港股）**：配置 `LONGBRIDGE_*` 后，美股与港股的日线与实时行情由 Longbridge 优先拉取；若失败或字段缺失，再由 YFinance / AkShare 兜底或补全。未配置长桥凭据时不会调用 Longbridge。详见 `.env.example` 与 [完整配置与部署指南](docs/full-guide.md)。

## 🚀 快速开始

### 方式一：GitHub Actions（推荐）

> 5 分钟完成部署，零成本，无需服务器。

1. Fork 本仓库
2. 进入 `Settings` → `Secrets and variables` → `Actions`
3. 至少配置以下最小项：

| 配置项 | 作用 | 是否必需 |
|--------|------|:--------:|
| `AIHUBMIX_KEY` / `GEMINI_API_KEY` / `OPENAI_API_KEY` / `OLLAMA_API_BASE` | 任选一个可用模型入口 | ✅ |
| `STOCK_LIST` | 自选股列表，如 `600519,hk00700,AAPL` | ✅ |
| 任一通知渠道（如 `WECHAT_WEBHOOK_URL`、`FEISHU_WEBHOOK_URL`、`TELEGRAM_BOT_TOKEN`、`EMAIL_SENDER` + `EMAIL_PASSWORD`） | 接收分析结果 | ✅ |
| `TAVILY_API_KEYS` | 新闻搜索，推荐配置 | 推荐 |

4. 在 `Actions` 页面启用并手动运行一次 `每日股票分析`

> 详细 Secrets / Variables、通知渠道、定时任务、报告选项见 [完整配置与部署指南](docs/full-guide.md)
>
> 大模型接入、渠道模式、Vision、Ollama、高级 YAML 路由见 [LLM 配置指南](docs/LLM_CONFIG_GUIDE.md)

### 方式二：本地运行 / Docker

```bash
# 克隆项目
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 安装依赖
pip install -r requirements.txt

# 复制配置
cp .env.example .env

# 运行一次分析
python main.py
```

如果你更偏好 Docker、桌面端或云服务器部署，请直接跳到下方“运行与部署”对应文档。

## 🚀 运行与部署

### 常用本地命令

```bash
# 单次分析
python main.py

# 调试 / 干跑
python main.py --debug
python main.py --dry-run

# 定时模式
python main.py --schedule

# 启动 Web 管理界面
python main.py --serve
python main.py --serve-only

# 直接启动 FastAPI
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 常用部署入口

| 场景 | 文档 |
|------|------|
| GitHub Actions 零成本托管 | [完整配置与部署指南](docs/full-guide.md) |
| Docker / 服务器部署 | [部署指南](docs/DEPLOY.md) |
| 云服务器访问 WebUI | [云服务器 Web 界面访问指南](docs/deploy-webui-cloud.md) |
| 桌面端打包 | [桌面端打包说明](docs/desktop-package.md) |
| Bot / API / Agent / 通知专题 | [中文文档索引](docs/INDEX.md) |

## 📱 推送效果

### 决策仪表盘
```
🎯 2026-02-08 决策仪表盘
共分析3只股票 | 买入:0 | 观望:2 | 卖出:1

📊 分析结果摘要
⚪ 中钨高新(000657): 观望 | 评分 65 | 看多
⚪ 永鼎股份(600105): 观望 | 评分 48 | 震荡
🟡 新莱应材(300260): 卖出 | 评分 35 | 看空

⚪ 中钨高新 (000657)
📰 重要信息速览
💭 舆情情绪: 市场关注其AI属性与业绩高增长，情绪偏积极，但需消化短期获利盘和主力流出压力。
📊 业绩预期: 基于舆情信息，公司2025年前三季度业绩同比大幅增长，基本面强劲，为股价提供支撑。

🚨 风险警报:
风险点1：2月5日主力资金大幅净卖出3.63亿元，需警惕短期抛压。
风险点2：筹码集中度高达35.15%，表明筹码分散，拉升阻力可能较大。
```

### 大盘复盘
```
🎯 2026-01-10 大盘复盘

📊 主要指数
- 上证指数: 3250.12 (🟢+0.85%)
- 深证成指: 10521.36 (🟢+1.02%)
- 创业板指: 2156.78 (🟢+1.35%)

📈 市场概况
上涨: 3920 | 下跌: 1349 | 涨停: 155 | 跌停: 3

板块表现
领涨: 互联网服务、文化传媒、小金属
领跌: 保险、航空机场、光伏设备
```

## 📚 文档导航

| 主题 | 文档 |
|------|------|
| 中文文档总入口 | [docs/INDEX.md](docs/INDEX.md) |
| 完整配置 / GitHub Actions / 环境变量 | [docs/full-guide.md](docs/full-guide.md) |
| Docker / 服务器部署 | [docs/DEPLOY.md](docs/DEPLOY.md) |
| LLM / 渠道模式 / Ollama / Vision | [docs/LLM_CONFIG_GUIDE.md](docs/LLM_CONFIG_GUIDE.md) |
| FAQ / 排障 | [docs/FAQ.md](docs/FAQ.md) |
| Bot 命令与集成 | [docs/bot-command.md](docs/bot-command.md) |
| 桌面端打包 | [docs/desktop-package.md](docs/desktop-package.md) |
| 贡献指南 | [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) |

> 若你需要 Web 交互细节、Agent 说明、导入能力、专题配置或部署排障，请从以上专题文档继续阅读。

## 🗺️ Roadmap

查看已支持的功能和未来规划：[更新日志](docs/CHANGELOG.md)

> 有建议？欢迎 [提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

---

## ☕ 支持项目

如果本项目对你有帮助，欢迎支持项目的持续维护与迭代，感谢支持 🙏  
赞赏可备注联系方式，祝股市长虹

| 支付宝 (Alipay) | 微信支付 (WeChat) | 小红书 |
| :---: | :---: | :---: |
| <img src="./sources/alipay.jpg" width="200" alt="Alipay"> | <img src="./sources/wechatpay.jpg" width="200" alt="WeChat Pay"> | <img src="./sources/xiaohongshu.png" width="200" alt="小红书"> |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详见 [贡献指南](docs/CONTRIBUTING.md)

### 本地门禁（建议先跑）

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
```

如修改前端（`apps/dsa-web`）：

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

## 📄 License
[MIT License](LICENSE) © 2026 ZhuLinsen

如果你在项目中使用或基于本项目进行二次开发，
非常欢迎在 README 或文档中注明来源并附上本仓库链接。
这将有助于项目的持续维护和社区发展。

## 📬 联系与合作
- GitHub Issues：[提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
- 合作邮箱：zhuls345@gmail.com

## ⭐ Star History
**如果觉得有用，请给个 ⭐ Star 支持一下！**

<a href="https://star-history.com/#ZhuLinsen/daily_stock_analysis&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
 </picture>
</a>

## ⚠️ 免责声明

本项目仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。作者不对使用本项目产生的任何损失负责。

---
