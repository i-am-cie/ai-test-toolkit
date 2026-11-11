# AI Test Toolkit

> 一套基于本地大模型（Ollama + Qwen2.5）的软件测试工具链，覆盖从需求分析到性能测试的完整测试生命周期。全部离线运行，不依赖任何云端 API Key。

## 🧭 工具总览

| 测试阶段 | 工具 | 端口 | 功能 |
| --- | --- | --- | --- |
| 需求分析 | [ai-test-generator](https://github.com/i-am-cie/ai-test-generator) | 5000 | 从需求/代码生成结构化测试用例，支持 JSON / CSV 导出 |
| 代码审查 | [code-review-assistant](https://github.com/i-am-cie/code-review-assistant) | 5001 | 全面 / 安全 / 风格三种模式的本地代码审查 |
| 接口测试 | [api-test-assistant](https://github.com/i-am-cie/api-test-assistant) | 5002 | 生成 API 测试用例、自动发送请求、AI 分析测试结果 |
| 数据测试 | [sql-test-assistant](https://github.com/i-am-cie/sql-test-assistant) | 5003 | 数据质量检查 SQL、测试用例生成、表结构审查 |
| UI 自动化 | [e2e-test-generator](https://github.com/i-am-cie/e2e-test-generator) | 5004 | 生成 Selenium / Playwright 端到端测试脚本 |
| 性能测试 | [perf-test-assistant](https://github.com/i-am-cie/perf-test-assistant) | 5005 | 生成 Locust 脚本、测试策略设计、压测结果分析 |

## 🔗 导航页面

仓库根目录的 [`index.html`](index.html) 是一个纯静态导航门户，卡片化展示上面 6 个工具，可直接通过 GitHub Pages 发布：

- 仓库 Settings → Pages → Source 选择 `main` 分支根目录即可
- 或本地直接双击 `index.html` 在浏览器打开

## 🏗️ 技术栈

- **后端**：Python 3 + Flask（每个工具一个独立 Web 服务）
- **大模型**：Ollama 本地运行 Qwen2.5:7b，所有推理在本机完成
- **前端**：原生 HTML + CSS + JavaScript，无构建依赖
- **数据隐私**：不上传任何代码、接口或测试数据到外部服务

## 🚀 本地运行

前置条件：安装 [Ollama](https://ollama.com/) 并拉取模型：

```bash
ollama pull qwen2.5:7b
```

进入任意工具目录后：

```bash
pip install -r requirements.txt
python app.py
```

然后浏览器访问对应端口（见上表）。

## 📐 工具链定位

```
需求文档 ──▶ 测试用例 ──▶ 代码审查 ──▶ 接口测试 ──▶ 数据校验 ──▶ UI 自动化 ──▶ 性能压测
   │            │            │            │            │            │            │
 ai-test-   code-review  api-test-  sql-test-  e2e-test-  perf-test-
 generator  -assistant    assistant  assistant  generator   assistant
```

每个工具独立可用，也可以按测试流程串联使用。

## 📝 License

MIT
