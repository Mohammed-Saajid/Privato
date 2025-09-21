"""Main entry point for the Privato CLI."""
from typer import Typer
from cli.commands import analyzer, redactor

app = Typer(
    name="privato",
    help="Privato CLI - A command line interface for managing private data securely.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True
)


app.add_typer(analyzer.analyzer_app, name="analyzer", help="Analyze files and directories for private data.")
app.add_typer(redactor.redactor_app, name="redactor", help="Redact files and directories to remove private data.")
if __name__ == "__main__":
    app()  
