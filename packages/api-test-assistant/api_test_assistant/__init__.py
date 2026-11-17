"""api-test-assistant: Generate and run API tests using local Ollama."""

from flask import Flask, request, jsonify
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import API_TEST_GENERATION_PROMPT, API_RUN_PROMPT
import requests
import json

app = Flask(__name__)

config = TLMConfig(model="qwen2.5:7b")
client = TLMClient(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>API Test Assistant</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        textarea { width: 100%; min-height: 300px; font-family: monospace; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        select, button, input { padding: 10px 15px; border-radius: 4px; border: 1px solid #ddd; }
        button { background: #17a2b8; color: white; border: none; cursor: pointer; }
        button:hover { background: #138496; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .output { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 300px; overflow: auto; }
        .error { color: #dc3545; }
        label { display: block; margin: 10px 0 5px; font-weight: 500; }
    </style>
</head>
<body>
    <h1>🌐 API Test Assistant</h1>
    <p>Generate and run API tests using local Ollama</p>
    
    <div class="container">
        <div>
            <label>模式</label>
            <select id="mode">
                <option value="generate">生成测试用例</option>
                <option value="run">运行测试并分析</option>
            </select>
            
            <label>API 基础 URL (运行模式需要)</label>
            <input type="text" id="baseUrl" placeholder="http://localhost:8000" />
            
            <label>API 描述 / 测试结果</label>
            <textarea id="input" placeholder="描述 API 或粘贴测试结果..."></textarea>
            
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
                const res = await fetch('/api/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        mode: document.getElementById('mode').value,
                        baseUrl: document.getElementById('baseUrl').value,
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

@app.route("/api/test", methods=["POST"])
def test():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400
    
    mode = data.get("mode", "generate")
    base_url = data.get("baseUrl", "")
    input_text = data.get("input", "")
    
    if not input_text.strip():
        return jsonify({"error": "Input cannot be empty"}), 400
    
    try:
        if mode == "generate":
            prompt = API_TEST_GENERATION_PROMPT.format(desc=input_text)
            result = client.chat([
                {"role": "system", "content": "You are an API testing expert."},
                {"role": "user", "content": prompt}
            ])
            return jsonify({"result": result.message.content})
        
        elif mode == "run":
            # Parse test cases from input (JSON array)
            try:
                test_cases = json.loads(input_text)
            except json.JSONDecodeError:
                return jsonify({"error": "Input must be valid JSON array of test cases"}), 400
            
            if not base_url:
                return jsonify({"error": "Base URL required for run mode"}), 400
            
            results = []
            for tc in test_cases:
                try:
                    url = base_url.rstrip('/') + '/' + tc.get('url', '').lstrip('/')
                    method = tc.get('method', 'GET').upper()
                    headers = tc.get('headers', {})
                    params = tc.get('params', {})
                    expected_status = tc.get('expected_status', 200)
                    
                    resp = requests.request(method, url, params=params, headers=headers, timeout=30)
                    
                    passed = resp.status_code == expected_status
                    results.append({
                        "name": tc.get('name', ''),
                        "method": method,
                        "url": url,
                        "expected_status": expected_status,
                        "actual_status": resp.status_code,
                        "passed": passed,
                        "response_time": resp.elapsed.total_seconds(),
                        "response_preview": resp.text[:500]
                    })
                except Exception as e:
                    results.append({
                        "name": tc.get('name', ''),
                        "error": str(e),
                        "passed": False
                    })
            
            # Analyze results with AI
            prompt = API_RUN_PROMPT.format(results=json.dumps(results, ensure_ascii=False, indent=2))
            analysis = client.chat([
                {"role": "system", "content": "You are a test analysis expert."},
                {"role": "user", "content": prompt}
            ])
            
            summary = {
                "total": len(results),
                "passed": sum(1 for r in results if r.get('passed')),
                "failed": sum(1 for r in results if not r.get('passed')),
                "results": results,
                "analysis": analysis.message.content
            }
            return jsonify({"result": json.dumps(summary, ensure_ascii=False, indent=2)})
        
        else:
            return jsonify({"error": "Invalid mode"}), 400
    
    except TLMError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": config.model})

def main():
    import argparse
    parser = argparse.ArgumentParser(description="API Test Assistant")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5002)
    parser.add_argument("--model", default="qwen2.5:7b")
    args = parser.parse_args()
    
    global config, client
    config = TLMConfig(model=args.model)
    client = TLMClient(config)
    
    print(f"Starting API Test Assistant on {args.host}:{args.port} with model {args.model}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
