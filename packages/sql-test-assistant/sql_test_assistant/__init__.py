"""sql-test-assistant: Generate SQL test cases and review schemas using local Ollama."""

from flask import Flask, request, jsonify
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import (
    DATA_QUALITY_SQL_PROMPT,
    SQL_TEST_GENERATION_PROMPT,
    SQL_PERFORMANCE_PROMPT,
    SCHEMA_REVIEW_PROMPT,
)

app = Flask(__name__)

config = TLMConfig(model="qwen2.5:7b")
client = TLMClient(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SQL Test Assistant</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        textarea { width: 100%; min-height: 300px; font-family: monospace; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        select, button { padding: 10px 15px; border-radius: 4px; border: 1px solid #ddd; }
        button { background: #6f42c1; color: white; border: none; cursor: pointer; }
        button:hover { background: #5a32a3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .output { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 300px; overflow: auto; }
        .error { color: #dc3545; }
        label { display: block; margin: 10px 0 5px; font-weight: 500; }
    </style>
</head>
<body>
    <h1>🗄️ SQL Test Assistant</h1>
    <p>Generate SQL test cases and review schemas using local Ollama</p>
    
    <div class="container">
        <div>
            <label>模式</label>
            <select id="mode">
                <option value="data_quality">数据质量检查 SQL</option>
                <option value="test_generation">测试用例生成</option>
                <option value="performance">性能分析</option>
                <option value="schema_review">表结构审查</option>
            </select>
            
            <label>输入描述 / SQL / Schema</label>
            <textarea id="input" placeholder="描述需求、粘贴 SQL 或表结构..."></textarea>
            
            <button id="submit" onclick="submit()">执行</button>
        </div>
        
        <div>
            <label>结果</label>
            <div id="output" class="output">等待执行...</div>
        </div>
    </div>

    <script>
        async function submit() {
            const btn = document.getElementById('submit');
            const output = document.getElementById('output');
            btn.disabled = true;
            output.textContent = '执行中...';
            
            try {
                const res = await fetch('/api/sql', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        mode: document.getElementById('mode').value,
                        input: document.getElementById('input').value
                    })
                });
                const data = await res.json();
                output.textContent = data.result || data.error;
                if (data.error) output.classList.add('error');
            } catch (e) {
                output.textContent = '错误: ' + e.message;
                output.classList.add('error');
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML_TEMPLATE

@app.route("/api/sql", methods=["POST"])
def sql():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400
    
    mode = data.get("mode", "data_quality")
    input_text = data.get("input", "")
    
    if not input_text.strip():
        return jsonify({"error": "Input cannot be empty"}), 400
    
    try:
        if mode == "data_quality":
            prompt = DATA_QUALITY_SQL_PROMPT.format(desc=input_text)
        elif mode == "test_generation":
            prompt = SQL_TEST_GENERATION_PROMPT.format(desc=input_text)
        elif mode == "performance":
            prompt = SQL_PERFORMANCE_PROMPT.format(sql=input_text)
        elif mode == "schema_review":
            prompt = SCHEMA_REVIEW_PROMPT.format(schema=input_text)
        else:
            return jsonify({"error": "Invalid mode"}), 400
        
        result = client.chat([
            {"role": "system", "content": "You are a database testing expert."},
            {"role": "user", "content": prompt}
        ])
        
        return jsonify({"result": result.message.content})
    
    except TLMError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": config.model})

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SQL Test Assistant")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5003)
    parser.add_argument("--model", default="qwen2.5:7b")
    args = parser.parse_args()
    
    global config, client
    config = TLMConfig(model=args.model)
    client = TLMClient(config)
    
    print(f"Starting SQL Test Assistant on {args.host}:{args.port} with model {args.model}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
