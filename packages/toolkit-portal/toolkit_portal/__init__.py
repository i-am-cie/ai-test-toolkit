"""toolkit-portal: Unified web portal for AI Test Toolkit."""

from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Tool configurations
TOOLS = [
    {
        "id": "ai-test-generator",
        "name": "AI Test Generator",
        "icon": "🤖",
        "description": "Generate unit tests, test plans, edge cases from code/requirements",
        "port": 5000,
        "color": "#007bff",
    },
    {
        "id": "code-review-assistant",
        "name": "Code Review Assistant",
        "icon": "🔍",
        "description": "Full code review: correctness, security, performance, style",
        "port": 5001,
        "color": "#28a745",
    },
    {
        "id": "api-test-assistant",
        "name": "API Test Assistant",
        "icon": "🌐",
        "description": "Generate and run API test cases with analysis",
        "port": 5002,
        "color": "#17a2b8",
    },
    {
        "id": "sql-test-assistant",
        "name": "SQL Test Assistant",
        "icon": "🗄️",
        "description": "Data quality checks, test generation, performance, schema review",
        "port": 5003,
        "color": "#6f42c1",
    },
    {
        "id": "e2e-test-generator",
        "name": "E2E Test Generator",
        "icon": "🎭",
        "description": "Generate Selenium/Playwright E2E test scripts",
        "port": 5004,
        "color": "#fd7e14",
    },
    {
        "id": "perf-test-assistant",
        "name": "Perf Test Assistant",
        "icon": "⚡",
        "description": "Performance test plans, Locust scripts, analysis templates",
        "port": 5005,
        "color": "#e83e8c",
    },
]

PORTAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Test Toolkit - Unified Portal</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .header {
            text-align: center;
            padding: 60px 20px 40px;
            color: white;
        }
        .header h1 { font-size: 3rem; margin: 0 0 10px; font-weight: 700; }
        .header p { font-size: 1.2rem; opacity: 0.9; margin: 0; }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 0 20px 60px;
        }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .tool-card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            transition: transform 0.2s, box-shadow 0.2s;
            text-decoration: none;
            color: inherit;
            display: block;
            position: relative;
            overflow: hidden;
        }
        .tool-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: var(--tool-color);
        }
        .tool-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        .tool-icon { font-size: 3rem; margin-bottom: 15px; display: block; }
        .tool-name { font-size: 1.4rem; font-weight: 600; margin: 0 0 10px; }
        .tool-desc { color: #666; line-height: 1.6; margin: 0; }
        .tool-status {
            display: inline-block;
            margin-top: 20px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .status-running { background: #d4edda; color: #155724; }
        .status-stopped { background: #f8d7da; color: #721c24; }
        .footer {
            text-align: center;
            padding: 30px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9rem;
        }
        .footer a { color: white; text-decoration: underline; }
    </style>
</head>
<body>
    <header class="header">
        <h1>AI Test Toolkit</h1>
        <p>6 Local AI-Powered Testing Tools • Powered by Ollama • Zero Cloud Dependency</p>
    </header>
    
    <div class="container">
        <div class="tools-grid">
            {% for tool in tools %}
            <a href="http://localhost:{{ tool.port }}" class="tool-card" target="_blank" style="--tool-color: {{ tool.color }};">
                <span class="tool-icon">{{ tool.icon }}</span>
                <h3 class="tool-name">{{ tool.name }}</h3>
                <p class="tool-desc">{{ tool.description }}</p>
                <span class="tool-status status-stopped">点击启动 (端口 {{ tool.port }})</span>
            </a>
            {% endfor %}
        </div>
    </div>
    
    <footer class="footer">
        <p>GitHub: <a href="https://github.com/i-am-cie/ai-test-toolkit" target="_blank">i-am-cie/ai-test-toolkit</a> | 
        共享核心: <code>tlm-client</code> + <code>prompt-templates</code> | 
        统一模型: <code>qwen2.5:7b</code></p>
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(PORTAL_HTML, tools=TOOLS)

@app.route("/health")
def health():
    return {"status": "ok", "tools": len(TOOLS)}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Test Toolkit Portal")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5006)
    args = parser.parse_args()
    
    print(f"Starting AI Test Toolkit Portal on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
