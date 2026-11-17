#!/usr/bin/env python3
"""Generate placeholder images for documentation."""

from PIL import Image, ImageDraw, ImageFont
import os

DOCS_DIR = os.path.dirname(__file__)

# Color palette for tools
TOOL_COLORS = {
    "ai-test-generator": "#007bff",
    "code-review-assistant": "#28a745",
    "api-test-assistant": "#17a2b8",
    "sql-test-assistant": "#6f42c1",
    "e2e-test-generator": "#fd7e14",
    "perf-test-assistant": "#e83e8c",
    "toolkit-portal": "#6c757d",
}

TOOL_NAMES = {
    "ai-test-generator": "AI Test Generator",
    "code-review-assistant": "Code Review Assistant",
    "api-test-assistant": "API Test Assistant",
    "sql-test-assistant": "SQL Test Assistant",
    "e2e-test-generator": "E2E Test Generator",
    "perf-test-assistant": "Perf Test Assistant",
    "toolkit-portal": "Toolkit Portal",
}

TOOL_ICONS = {
    "ai-test-generator": "🤖",
    "code-review-assistant": "🔍",
    "api-test-assistant": "🌐",
    "sql-test-assistant": "🗄️",
    "e2e-test-generator": "🎭",
    "perf-test-assistant": "⚡",
    "toolkit-portal": "🏠",
}


def generate_placeholder(tool_id: str, width: int = 1200, height: int = 800):
    """Generate a placeholder image for a tool."""
    color = TOOL_COLORS.get(tool_id, "#6c757d")
    name = TOOL_NAMES.get(tool_id, tool_id)
    icon = TOOL_ICONS.get(tool_id, "🔧")
    
    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Draw colored bar at top
    draw.rectangle([0, 0, width, 8], fill=color)
    
    # Draw card-like area
    card_x, card_y = 100, 150
    card_w, card_h = width - 200, height - 300
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=16,
        fill='white',
        outline='#dee2e6',
        width=2
    )
    
    # Draw icon and name
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Icon
    icon_bbox = draw.textbbox((0, 0), icon, font=font_large)
    icon_w = icon_bbox[2] - icon_bbox[0]
    draw.text(
        (card_x + (card_w - icon_w) // 2, card_y + 60),
        icon,
        font=font_large,
        fill=color
    )
    
    # Name
    name_bbox = draw.textbbox((0, 0), name, font=font_medium)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text(
        (card_x + (card_w - name_w) // 2, card_y + 180),
        name,
        font=font_medium,
        fill='#212529'
    )
    
    # Placeholder text
    placeholder = "Screenshot Placeholder\nRun the tool locally to capture real UI"
    draw.multiline_text(
        (card_x + 50, card_y + 280),
        placeholder,
        font=font_small,
        fill='#adb5bd',
        align='center',
        spacing=10
    )
    
    # Footer
    footer = "AI Test Toolkit • Local AI Testing • Powered by Ollama"
    footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(
        (card_x + (card_w - footer_w) // 2, card_y + card_h - 60),
        footer,
        font=font_small,
        fill='#ced4da'
    )
    
    output_path = os.path.join(DOCS_DIR, f"{tool_id}.png")
    img.save(output_path)
    print(f"Generated: {output_path}")


def generate_banner(width: int = 1200, height: int = 400):
    """Generate banner image."""
    img = Image.new('RGB', (width, height), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Gradient effect (simulated)
    for y in range(height):
        ratio = y / height
        r = int(102 * (1 - ratio) + 118 * ratio)
        g = int(126 * (1 - ratio) + 75 * ratio)
        b = int(234 * (1 - ratio) + 162 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    # Title
    title = "AI Test Toolkit"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(
        ((width - title_w) // 2, height // 2 - 60),
        title,
        font=font_title,
        fill='white'
    )
    
    # Subtitle
    sub = "6 Local AI-Powered Testing Tools • Zero Cloud Dependency"
    sub_bbox = draw.textbbox((0, 0), sub, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(
        ((width - sub_w) // 2, height // 2 + 40),
        sub,
        font=font_sub,
        fill=(230, 230, 230)
    )
    
    output_path = os.path.join(DOCS_DIR, "banner.png")
    img.save(output_path)
    print(f"Generated: {output_path}")


def generate_portal_dashboard(width: int = 1200, height: int = 800):
    """Generate portal dashboard showing all 6 tools."""
    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([0, 0, width, 120], fill='#667eea')
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    draw.text((60, 20), "AI Test Toolkit Portal", font=font_title, fill='white')
    draw.text((60, 75), "6 Tools • Local Ollama • Unified Access", font=font_sub, fill=(230, 230, 230))
    
    # Tool cards grid (2x3)
    card_w, card_h = 340, 180
    start_x, start_y = 80, 160
    gap_x, gap_y = 40, 30
    
    tools = [
        ("ai-test-generator", "5000"),
        ("code-review-assistant", "5001"),
        ("api-test-assistant", "5002"),
        ("sql-test-assistant", "5003"),
        ("e2e-test-generator", "5004"),
        ("perf-test-assistant", "5005"),
    ]
    
    for i, (tool_id, port) in enumerate(tools):
        row = i // 3
        col = i % 3
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        
        color = TOOL_COLORS[tool_id]
        name = TOOL_NAMES[tool_id]
        icon = TOOL_ICONS[tool_id]
        
        # Card background
        draw.rounded_rectangle(
            [x, y, x + card_w, y + card_h],
            radius=12,
            fill='white',
            outline='#dee2e6',
            width=1
        )
        
        # Color bar
        draw.rounded_rectangle(
            [x, y, x + card_w, y + 6],
            radius=12,
            fill=color
        )
        
        try:
            font_icon = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            font_name = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            font_port = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            font_icon = ImageFont.load_default()
            font_name = ImageFont.load_default()
            font_port = ImageFont.load_default()
        
        # Icon
        icon_bbox = draw.textbbox((0, 0), icon, font=font_icon)
        icon_w = icon_bbox[2] - icon_bbox[0]
        draw.text((x + (card_w - icon_w) // 2, y + 20), icon, font=font_icon, fill=color)
        
        # Name
        name_bbox = draw.textbbox((0, 0), name, font=font_name)
        name_w = name_bbox[2] - name_bbox[0]
        draw.text((x + (card_w - name_w) // 2, y + 90), name, font=font_name, fill='#212529')
        
        # Port
        port_text = f"Port {port}"
        port_bbox = draw.textbbox((0, 0), port_text, font=font_port)
        port_w = port_bbox[2] - port_bbox[0]
        draw.text((x + (card_w - port_w) // 2, y + 130), port_text, font=font_port, fill='#6c757d')
    
    output_path = os.path.join(DOCS_DIR, "portal-dashboard.png")
    img.save(output_path)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    # Generate all placeholders
    generate_banner()
    generate_portal_dashboard()
    
    for tool_id in TOOL_COLORS:
        generate_placeholder(tool_id)
    
    print("\nAll placeholders generated in docs/")
