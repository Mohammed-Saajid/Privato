"""Module for ingesting and normalizing various file types."""
from typing import List, Union, Dict, Tuple, Any, Callable
from pathlib import Path
from PIL import Image
from pandas import DataFrame
from fastapi import UploadFile
from .converter import PDFToImageConverter
from .file_reader import FileReader


class Ingestor:
    """
    Handles ingestion of PDFs, images, or text into a consistent format.
    Converts PDFs to images, reads images, text files, Excel, CSV, and JSON files.
    Attributes:
        SUPPORTED_IMAGE_FORMATS (set): Supported image file extensions.
        SUPPORTED_FILE_FORMATS (set): Supported file extensions for ingestion.
    """
    SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
    SUPPORTED_TEXT_FORMATS = {".txt"}
    SUPPORTED_CSV_FORMATS = {".csv"}
    SUPPORTED_XLSX_FORMATS = {".xlsx"}
    SUPPORTED_JSON_FORMATS = {".json"}
    SUPPORTED_PDF_FORMATS = {".pdf"}

    SUPPORTED_FILE_FORMATS = (
        SUPPORTED_IMAGE_FORMATS |
        SUPPORTED_TEXT_FORMATS |
        SUPPORTED_CSV_FORMATS |
        SUPPORTED_XLSX_FORMATS |
        SUPPORTED_JSON_FORMATS |
        SUPPORTED_PDF_FORMATS
    )

    def __init__(self, dpi: int = 200):
        """Initialize the Ingestor with converters.
        Args:
            dpi (int, optional): DPI for PDF to image conversion. Defaults to 200.
        """
        self.pdf_to_image = PDFToImageConverter(dpi=dpi)
        self.file_reader = FileReader()
        self._handler_map = self._initialize_handlers()

    def _initialize_handlers(self) -> Dict[str, Callable]:
        """Initializes a dispatch map from extension to handler method.
        Returns:
            Dict[str, callable]: A mapping from file extensions to handler methods.
        """
        handlers = {ext: self._handle_image for ext in self.SUPPORTED_IMAGE_FORMATS}
        handlers.update({ext: self._handle_pdf for ext in self.SUPPORTED_PDF_FORMATS})
        handlers.update({ext: self._handle_text for ext in self.SUPPORTED_TEXT_FORMATS})
        handlers.update({ext: self._handle_xlsx for ext in self.SUPPORTED_XLSX_FORMATS})
        handlers.update({ext: self._handle_json for ext in self.SUPPORTED_JSON_FORMATS})
        handlers.update({ext: self._handle_csv for ext in self.SUPPORTED_CSV_FORMATS})
        return handlers

    def _handle_pdf(self, file_bytes: bytes) -> Tuple[List[Image.Image], str]:
        """Convert PDF bytes to a list of images.
        Args:
            file_bytes (bytes): The PDF file content in bytes.
        Returns:
            Tuple[List[Image.Image], str]: A tuple containing a list of images and the type 'imgs'.
        """
        image_paths = self.pdf_to_image.convert(file_bytes)
        images = [self.file_reader.read_image(p) for p in image_paths if p.exists()]
        return images, "imgs"

    def _handle_image(self, file_bytes: bytes) -> Tuple[Image.Image, str]:
        """Read image bytes into a PIL Image.
        Args:
            file_bytes (bytes): The image file content in bytes.
        Returns:
            Tuple[Image.Image, str]: A tuple containing the image and the type 'img'.
        """
        return self.file_reader.read_image(file_bytes), "img"

    def _handle_text(self, file_bytes: bytes) -> Tuple[str, str]:
        """Read text bytes into a string.
        Args:
            file_bytes (bytes): The text file content in bytes.
        Returns:
            Tuple[str, str]: A tuple containing the text and the type 'text'.
        """
        return self.file_reader.read_text(file_bytes), "text"

    def _handle_csv(self, file_bytes: bytes) -> Tuple[DataFrame, str]:
        """Read CSV bytes into a pandas DataFrame.
        Args:
            file_bytes (bytes): The CSV file content in bytes.
        Returns:
            Tuple[DataFrame, str]: A tuple containing the DataFrame and the type 'df'.
        """
        return self.file_reader.read_csv(file_bytes), "df"

    def _handle_xlsx(self, file_bytes: bytes) -> Tuple[DataFrame, str]:
        """Read XLSX bytes into a pandas DataFrame.
        Args:
            file_bytes (bytes): The XLSX file content in bytes.
        Returns:
            Tuple[DataFrame, str]: A tuple containing the DataFrame and the type 'df'.
        """
        return self.file_reader.read_xlsx(file_bytes), "df"

    def _handle_json(self, file_bytes: bytes) -> Tuple[List[Dict], str]:
        """Read JSON bytes into a dictionary or list of dictionaries.
        Args:
            file_bytes (bytes): The JSON file content in bytes.
        Returns:
            Tuple[List[Dict], str]: A tuple containing the JSON data and the type 'json'.
        """
        return [self.file_reader.read_json(file_bytes)], "json"
    
    def ingest_directory(self, dir_path: Path) -> List[Tuple[Any, str]]:
        """
        Ingest all supported files in a directory.
        Args:
            dir_path (Path): The directory path to ingest files from.
        Returns:
            List[Tuple[Any, str]]: A list of tuples containing ingested content and its type.
        """
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Provided path is not a directory: {dir_path}")

        ingested_files = []
        for file_path in dir_path.rglob('*'):
            if file_path.suffix.lower() in self.SUPPORTED_FILE_FORMATS:
                try:
                    ingested_content = self.ingest(file_path)
                    ingested_files.append(ingested_content)
                except Exception as e:
                    print(f"Error ingesting {file_path}: {e}")
        return ingested_files

    def ingest(self, file: Union[UploadFile, Path]) -> Tuple[Any, str]:
        """
        Ingest a document and normalize it into a list of content items.
        Args:
            file (Union[UploadFile, Path]): The uploaded file or file path to ingest.
        Returns:
            Tuple[List[Any], str]: A tuple containing a list of the ingested
            content and a string representing its type.
        """
        if isinstance(file, Path):
            if not file.exists():
                raise FileNotFoundError(f"Path not found: {file}")
            if file.is_dir():
                raise ValueError(f"Expected a file but got a directory: {file}. Use ingest_directory instead.")
            file_bytes = file.read_bytes()
            ext = file.suffix.lower()
        else: # isinstance(file, UploadFile)
            file_bytes = file.file.read()
            ext = f".{file.filename.split('.')[-1].lower()}"

        handler = self._handler_map.get(ext)
        if not handler:
            raise ValueError(f"Unsupported file type: {ext}")

        return handler(file_bytes)

