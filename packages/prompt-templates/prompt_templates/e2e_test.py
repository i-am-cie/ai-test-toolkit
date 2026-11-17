"""Prompt templates for E2E testing (e2e-test-generator)."""

E2E_TEST_GENERATION_PROMPT = """你是一个E2E测试专家。请根据以下需求生成完整的端到端测试脚本。

需求描述：
{desc}

请生成：
1. **测试场景设计**：用户旅程、关键路径、异常流程
2. **页面对象模型（POM）**：页面类、定位器、操作方法
3. **测试脚本**：
   - Selenium 版本（Python + pytest）
   - Playwright 版本（Python + pytest）
4. **测试数据**：测试账号、测试数据准备/清理
5. **CI/CD 集成**：GitHub Actions / GitLab CI 配置片段

每个脚本包含：
- 测试前置条件（登录、数据准备）
- 测试步骤（点击、输入、断言、等待）
- 测试后清理（登出、数据回滚）
- 失败重试、截图、日志记录

输出两套完整可运行的代码（Selenium + Playwright），用Markdown分隔。"""
