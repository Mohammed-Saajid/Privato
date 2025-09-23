from typer import Typer
import subprocess
import rich

app = Typer(
    name='api',
    help='Run Privato API',          
    )

@app.command("run", help="Run Privato API")
def run(
    port : int = 8080,
):
    rich.print(f"[bold green]Starting Privato API on port {port}...[/bold green]")
    rich.print("[bold yellow]Press Ctrl+C to stop the server.[/bold yellow]")
    rich.print(f"[bold blue]Open http://127.0.0.1:{port} in your browser to access the API.[/bold blue]")
    rich.print("[bold magenta]Note: The first startup may take a while as the models are being loaded.[/bold magenta]")
    rich.print("[bold cyan]Check the logs for more details.[/bold cyan]")
    subprocess.run(["uvicorn", "privato.app.main:app", "--host", "0.0.0.0", "--port", str(port)])
