"""code-review-assistant: AI-powered code review using local Ollama."""

from flask import Flask, request, jsonify
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import (
    FULL_REVIEW_PROMPT,
    SECURITY_REVIEW_PROMPT,
    STYLE_REVIEW_PROMPT,
)

app = Flask(__name__)

config = TLMConfig(model="qwen2.5:7b")
client = TLMClient(config)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Code Review Assistant</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; line-height: 1.6; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        textarea { width: 100%; min-height: 300px; font-family: monospace; font-size: 14px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        select, button { padding: 10px 15px; border-radius: 4px; border: 1px solid #ddd; }
        button { background: #28a745; color: white; border: none; cursor: pointer; }
        button:hover { background: #218838; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .output { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 300px; overflow: auto; }
        .error { color: #dc3545; }
        label { display: block; margin: 10px 0 5px; font-weight: 500; }
    </style>
</head>
<body>
    <h1>🔍 Code Review Assistant</h1>
    <p>AI-powered code review using local Ollama</p>
    
    <div class="container">
        <div>
            <label>审查类型</label>
            <select id="mode">
                <option value="full">全面审查</option>
                <option value="security">安全审查</option>
                <option value="style">风格审查</option>
            </select>
            
            <label>语言</label>
            <select id="language">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="go">Go</option>
            </select>
            
            <label>代码</label>
            <textarea id="input" placeholder="粘贴待审查的代码..."></textarea>
            
            <button id="review" onclick="review()">开始审查</button>
        </div>
        
        <div>
            <label>审查结果</label>
            <div id="output" class="output">等待审查...</div>
        </div>
    </div>

    <script>
        async function review() {
            const btn = document.getElementById('review');
            const output = document.getElementById('output');
            btn.disabled = true;
            output.textContent = '审查中...';
            
            try {
                const res = await fetch('/api/review', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        mode: document.getElementById('mode').value,
                        language: document.getElementById('language').value,
                        code: document.getElementById('input').value
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

@app.route("/api/review", methods=["POST"])
def review():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400
    
    mode = data.get("mode", "full")
    language = data.get("language", "python")
    code = data.get("code", "")
    
    if not code.strip():
        return jsonify({"error": "Code cannot be empty"}), 400
    
    try:
        if mode == "full":
            prompt = FULL_REVIEW_PROMPT.format(language=language, code=code)
        elif mode == "security":
            prompt = SECURITY_REVIEW_PROMPT.format(language=language, code=code)
        elif mode == "style":
            prompt = STYLE_REVIEW_PROMPT.format(language=language, code=code)
        else:
            return jsonify({"error": "Invalid mode"}), 400
        
        result = client.chat([
            {"role": "system", "content": "You are a senior code review expert."},
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
    parser = argparse.ArgumentParser(description="Code Review Assistant")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--model", default="qwen2.5:7b")
    args = parser.parse_args()
    
    global config, client
    config = TLMConfig(model=args.model)
    client = TLMClient(config)
    
    print(f"Starting Code Review Assistant on {args.host}:{args.port} with model {args.model}")
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
