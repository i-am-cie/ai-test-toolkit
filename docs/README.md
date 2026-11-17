# Documentation Assets

This directory contains screenshots, GIFs, and diagrams for the README.

## Required Assets

| File | Description | Size |
|------|-------------|------|
| `banner.png` | Top banner for README | 1200x400 |
| `portal.png` | Portal dashboard screenshot | 1200x800 |
| `portal-dashboard.png` | Portal dashboard detail | 1200x800 |
| `ai-test-generator.png` | AI Test Generator web UI | 1200x800 |
| `code-review-security.png` | Code Review security mode | 1200x800 |
| `api-test-assistant.png` | API Test Assistant | 1200x800 |
| `sql-test-assistant.png` | SQL Test Assistant | 1200x800 |
| `e2e-test-generator.png` | E2E Test Generator | 1200x800 |
| `perf-test-assistant.png` | Perf Test Assistant | 1200x800 |
| `cli-demo.gif` | CLI interaction demo | 800x600 |

## How to Capture

```bash
# Start portal
uv run toolkit-portal

# Start individual tools
uv run ai-test-generator &
uv run code-review-assistant &
# ... etc

# Take screenshots (macOS)
screencapture -x docs/portal.png

# Record GIF (using ffmpeg or similar)
# ffmpeg -f x11grab -r 10 -s 800x600 -i :0.0 -vf "fps=10,scale=800:-1" docs/cli-demo.gif
```

## Placeholder Generation

For quick placeholders, you can use:
- [Placeholder.com](https://placeholder.com)
- [Via.placeholder.com](https://via.placeholder.com)
- Generate with Python PIL

Example:
```python
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (1200, 800), color='#f0f0f0')
draw = ImageDraw.Draw(img)
draw.text((100, 100), "Screenshot Placeholder", fill='#999')
img.save('docs/portal.png')
```
