"""Entry Point for the Privato CLI Analyzer."""
from typer import Typer, Argument, Option
import typer
from core.analyzer import Analyzer
from core.ingestion import Ingestor
from pathlib import Path
from core.config import logger,SUPPORTED_LANGUAGES
from typing import Dict, List,Union
import rich
from core.save_files import SaveFiles

analyzer_app = Typer(
    name="analyzer",
    help="Analyze files and directories for private data.",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True
)

@analyzer_app.command("analyze", help="Analyze a file or directory for Personally Identifiable Information.")
def analyze(
    path: Path = Argument(..., help="The file or directory to analyze."),
    language: str = Option("en", help="Language of the content, e.g., 'en' for English."),
    hide_output: bool = Option(False, help="Hide the analysis result from the console.", show_default=True),
    save_output: bool = Option(False, help="Save the analysis result to a JSON file.", show_default=True),
    output_path: Path = Option(None, help="The output file path to save the analysis result if --save-output is set."),
    ):
    
    """Analyze a file or directory for Personally Identifiable Information.
    Args:
        path (Path): Path to the file or directory to be analyzed.
        language (str, optional): Language of the content. Defaults to "en".
    Returns:

    """
    analyzer = Analyzer()
    ingestor = Ingestor()
    
    try:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError("Language Not Supported. Atleast Not yet. Supported languages are: " + ", ".join(SUPPORTED_LANGUAGES))
        if path.is_dir():
            files = ingestor.ingest_directory(path)
            analysis_result = analyzer.analyze_files(files,language=language)
        elif not path.is_file():
            raise ValueError(f"The provided path is neither a file nor a directory: {path}")
        else:
            ingested_file,ext = ingestor.ingest(path)
            analysis_result = analyzer.analyze(ingested_file,data_type=ext,language=language)
        if save_output:
            if not output_path:
                output_path = path.with_suffix('.analysis.json') if path.is_file() else path / 'analysis.json'
            elif output_path.is_dir():
                output_path = output_path / (path.stem + '.analysis.json' if path.is_file() else 'analysis.json')
            saver = SaveFiles(output_path.parent)
            saver.save(analysis_result, data_type="json", filename=output_path.stem)
            rich.print(f"Analysis result saved to {output_path}")
        if not hide_output:
            rich.print(analysis_result)
        
    except Exception as e:
        logger.error(f"Error during file analysis: {e}")
        raise typer.Exit(code=1)


