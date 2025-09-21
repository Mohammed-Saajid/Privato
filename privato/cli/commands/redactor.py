"""Entry Point for the Privato CLI Redactor."""

from typer import Typer, Argument, Option
import typer
from privato.core.redactor import Redactor
from privato.core.ingestion import Ingestor
from privato.core.save_files import SaveFiles
from pathlib import Path
from privato.core.config import logger
from typing import Dict, List, Union, Any
from privato.core.utils import get_dir_files_names
from privato.core.config import SUPPORTED_LANGUAGES

redactor_app = Typer(
    name="redactor",
    help="Redact files and directories containing private data.",
    rich_markup_mode="rich",
    add_completion=False,
    pretty_exceptions_enable=True,
    pretty_exceptions_show_locals=True,
    pretty_exceptions_short=True
)

@redactor_app.command("redact", help="Redact a file or directory containing Personally Identifiable Information.")
def redact(
    input_path: Path = Argument(..., help="The file or directory to redact.", exists=True),
    output_path: Path = Argument(..., help="The output file or directory for the redacted content."),
    language: str = Option("en", help="Language of the content, e.g., 'en' for English."),
):
    """Redact the specified file or directory."""
    logger.info(f"Redacting {input_path}...")
    redactor = Redactor()
    ingestor = Ingestor()
    saver = SaveFiles(output_path)
    file_names: List[str] = []
    files : List[tuple[Any, str]] = []

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError("Language Not Supported. Atleast Not yet. Supported languages are: " + ", ".join(SUPPORTED_LANGUAGES))
    try:
        if output_path.is_file():
            raise ValueError(f"Output path {output_path} cannot be a file.")
        if not output_path.exists():
                output_path.mkdir(parents=True, exist_ok=True)
        if input_path.is_dir():
            files.extend(ingestor.ingest_directory(input_path))
            file_names.extend(get_dir_files_names(input_path))
        elif input_path.is_file():
            files.append(ingestor.ingest(input_path))
            file_names.append(input_path.stem)
        else:
            raise ValueError(f"The provided path is neither a file nor a directory: {input_path}")

        assert len(files) == len(file_names), "Mismatch between number of files and filenames."

        redacted_files = redactor.redact_files(files, language=language)
        saver.save_files(redacted_files, filenames=file_names)

        logger.info(f"Redaction complete. Output saved to {output_path}.")
    except Exception as e:
        logger.error(f"Error during redaction: {e}")
        raise typer.Exit(code=1)