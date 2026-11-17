"""CLI entry point for ai-test-generator."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from tlm_client import TLMClient, TLMConfig, TLMError
from prompt_templates import (
    UNIT_TEST_PROMPT,
    TEST_PLAN_PROMPT,
    EDGE_CASES_PROMPT,
    STRUCTURED_TEST_CASES_PROMPT,
)

app = typer.Typer(help="AI Test Generator - Generate tests from code/requirements")
console = Console()

MODES = {
    "unit": ("单元测试生成", UNIT_TEST_PROMPT, ["language", "code"]),
    "plan": ("测试计划生成", TEST_PLAN_PROMPT, ["test_type", "requirement"]),
    "edge": ("边界值测试", EDGE_CASES_PROMPT, ["input_desc"]),
    "structured": ("结构化测试用例", STRUCTURED_TEST_CASES_PROMPT, ["requirement"]),
}

@app.command()
def generate(
    mode: str = typer.Option("unit", "--mode", "-m", help="Generation mode"),
    language: str = typer.Option("python", "--lang", "-l", help="Programming language"),
    model: str = typer.Option("qwen2.5:7b", "--model", help="Ollama model"),
    host: str = typer.Option("http://localhost:11434", "--host", help="Ollama host"),
    input_file: str = typer.Option(None, "--file", "-f", help="Input file path"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
):
    """Generate test cases."""
    
    if mode not in MODES:
        console.print(f"[red]Invalid mode. Choose from: {', '.join(MODES.keys())}[/red]")
        raise typer.Exit(1)
    
    config = TLMConfig(model=model, host=host)
    client = TLMClient(config)
    
    # Get input
    if input_file:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
    elif interactive:
        console.print(Panel(f"[bold]{MODES[mode][0]}[/bold]", style="cyan"))
        if mode == "unit":
            language = Prompt.ask("Language", default=language)
            console.print("Paste code (Ctrl+D to finish):")
            input_text = console.input("")
        elif mode == "plan":
            input_text = Prompt.ask("Requirement description")
        elif mode == "edge":
            input_text = Prompt.ask("Input description")
        elif mode == "structured":
            input_text = Prompt.ask("Requirement description")
    else:
        console.print("[yellow]No input provided. Use --file or --interactive[/yellow]")
        raise typer.Exit(1)
    
    # Build prompt
    _, template, vars_needed = MODES[mode]
    format_args = {"language": language}
    if "code" in vars_needed:
        format_args["code"] = input_text
    if "requirement" in vars_needed:
        format_args["requirement"] = input_text
    if "test_type" in vars_needed:
        format_args["test_type"] = "测试"
    if "input_desc" in vars_needed:
        format_args["input_desc"] = input_text
    
    prompt = template.format(**format_args)
    
    # Generate
    console.print(f"[cyan]Generating with {model}...[/cyan]")
    try:
        result = client.chat([
            {"role": "system", "content": "You are a senior test engineer."},
            {"role": "user", "content": prompt}
        ])
        console.print(Panel(result.message.content, title="Generated Output", style="green"))
    except TLMError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(5000, "--port"),
    model: str = typer.Option("qwen2.5:7b", "--model"),
):
    """Start web server."""
    import subprocess
    subprocess.run([
        "python", "-m", "ai_test_generator.app",
        "--host", host, "--port", str(port), "--model", model
    ])

if __name__ == "__main__":
    app()
