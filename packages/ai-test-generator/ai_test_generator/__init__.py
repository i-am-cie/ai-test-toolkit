"""ai-test-generator: Generate test cases from code/requirements using local Ollama."""

from flask import Flask, request, jsonify, render_template_string
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import (
    UNIT_TEST_PROMPT,
    TEST_PLAN_PROMPT,
    EDGE_CASES_PROMPT,
    STRUCTURED_TEST_CASES_PROMPT,
)

app = Flask(__name__)

# Default configuration
config = TLMConfig(model="qwen2.5:7b")
client = TLMClient(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Test Generator</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        textarea { width: 100%; min-height: 300px; font-family: monospace; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        select, button { padding: 10px 15px; border-radius: 4px; border: 1px solid #ddd; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .output { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 300px; overflow: auto; }
        .error { color: #dc3545; }
        label { display: block; margin: 10px 0 5px; font-weight: 500; }
    </style>
</head>
<body>
    <h1>🤖 AI Test Generator</h1>
    <p>Generate test cases from code or requirements using local Ollama</p>
    
    <div class="container">
        <div>
            <label>模式</label>
            <select id="mode">
                <option value="unit">单元测试生成</option>
                <option value="plan">测试计划生成</option>
                <option value="edge">边界值测试</option>
                <option value="structured">结构化测试用例</option>
            </select>
            
            <label>语言</label>
            <select id="language">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="go">Go</option>
            </select>
            
            <label>输入代码/需求</label>
            <textarea id="input" placeholder="粘贴代码或描述需求..."></textarea>
            
            <button id="generate" onclick="generate()">生成测试</button>
        </div>
        
        <div>
            <label>输出结果</label>
            <div id="output" class="output">等待生成...</div>
        </div>
    </div>

    <script>
        async function generate() {
            const btn = document.getElementById('generate');
            const output = document.getElementById('output');
            btn.disabled = true;
            output.textContent = '生成中...';
            
            try {
                const res = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        mode: document.getElementById('mode').value,
                        language: document.getElementById('language').value,
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

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400
    
    mode = data.get("mode", "unit")
    language = data.get("language", "python")
    input_text = data.get("input", "")
    
    if not input_text.strip():
        return jsonify({"error": "Input cannot be empty"}), 400
    
    try:
        if mode == "unit":
            prompt = UNIT_TEST_PROMPT.format(language=language, code=input_text)
        elif mode == "plan":
            prompt = TEST_PLAN_PROMPT.format(test_type="测试", requirement=input_text)
        elif mode == "edge":
            prompt = EDGE_CASES_PROMPT.format(input_desc=input_text)
        elif mode == "structured":
            prompt = STRUCTURED_TEST_CASES_PROMPT.format(requirement=input_text)
        else:
            return jsonify({"error": "Invalid mode"}), 400
        
        result = client.chat([
            {"role": "system", "content": "You are a senior test engineer."},
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
    parser = argparse.ArgumentParser(description="AI Test Generator")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--model", default="qwen2.5:7b")
    args = parser.parse_args()
    
    global config, client
    config = TLMConfig(model=args.model)
    client = TLMClient(config)
    
    print(f"Starting AI Test Generator on {args.host}:{args.port} with model {args.model}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
