"""e2e-test-generator: Generate E2E test scripts using local Ollama."""

from flask import Flask, request, jsonify
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import E2E_TEST_GENERATION_PROMPT

app = Flask(__name__)

config = TLMConfig(model="qwen2.5:7b")
client = TLMClient(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>E2E Test Generator</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        textarea { width: 100%; min-height: 300px; font-family: monospace; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 10px 15px; border-radius: 4px; border: none; background: #fd7e14; color: white; cursor: pointer; }
        button:hover { background: #e8650e; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .output { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 300px; overflow: auto; }
        .error { color: #dc3545; }
        label { display: block; margin: 10px 0 5px; font-weight: 500; }
    </style>
</head>
<body>
    <h1>🎭 E2E Test Generator</h1>
    <p>Generate E2E test scripts (Selenium/Playwright) using local Ollama</p>
    
    <div class="container">
        <div>
            <label>需求描述</label>
            <textarea id="input" placeholder="描述待测试的用户旅程/功能..."></textarea>
            
            <button id="generate" onclick="generate()">生成 E2E 测试</button>
        </div>
        
        <div>
            <label>生成的测试脚本</label>
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
                    body: JSON.stringify({input: document.getElementById('input').value})
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
    
    input_text = data.get("input", "")
    
    if not input_text.strip():
        return jsonify({"error": "Input cannot be empty"}), 400
    
    try:
        prompt = E2E_TEST_GENERATION_PROMPT.format(desc=input_text)
        result = client.chat([
            {"role": "system", "content": "You are an E2E testing expert."},
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
    parser = argparse.ArgumentParser(description="E2E Test Generator")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5004)
    parser.add_argument("--model", default="qwen2.5:7b")
    args = parser.parse_args()
    
    global config, client
    config = TLMConfig(model=args.model)
    client = TLMClient(config)
    
    print(f"Starting E2E Test Generator on {args.host}:{args.port} with model {args.model}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
