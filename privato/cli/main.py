"""Main entry point for the Privato CLI."""
from typer import Typer
from privato.cli.commands import analyzer, redactor, api

app = Typer(
    name="privato",
    help="Privato CLI - A command line interface for Analyzing and Redacting personally identifiable information.",
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True
)


app.add_typer(analyzer.analyzer_app, name="analyzer", help="Analyze files and directories for private data.")
app.add_typer(redactor.redactor_app, name="redactor", help="Redact files and directories to remove private data.")
app.add_typer(api.app, name="api", help="Run Privato API.")
if __name__ == "__main__":
    app()  
