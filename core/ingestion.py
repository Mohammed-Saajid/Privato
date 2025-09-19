"""Module for ingesting and normalizing various file types."""
from typing import List, Union, Dict, Tuple, Any, Callable
from pathlib import Path
from PIL import Image
from pandas import DataFrame
from fastapi import UploadFile
from io import BytesIO
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
        """Initializes a dispatch map from extension to handler method."""
        handlers = {ext: self._handle_image for ext in self.SUPPORTED_IMAGE_FORMATS}
        handlers.update({ext: self._handle_pdf for ext in self.SUPPORTED_PDF_FORMATS})
        handlers.update({ext: self._handle_text for ext in self.SUPPORTED_TEXT_FORMATS})
        handlers.update({ext: self._handle_xlsx for ext in self.SUPPORTED_XLSX_FORMATS})
        handlers.update({ext: self._handle_json for ext in self.SUPPORTED_JSON_FORMATS})
        handlers.update({ext: self._handle_csv for ext in self.SUPPORTED_CSV_FORMATS})
        return handlers

    def _handle_pdf(self, file_bytes: bytes) -> Tuple[List[Image.Image], str]:
        image_paths = self.pdf_to_image.convert(file_bytes)
        images = [self.file_reader.read_image(p) for p in image_paths if p.exists()]
        return images, "imgs"

    def _handle_image(self, file_bytes: bytes) -> Tuple[Image.Image, str]:
        return self.file_reader.read_image(file_bytes), "img"

    def _handle_text(self, file_bytes: bytes) -> Tuple[str, str]:
        return self.file_reader.read_text(file_bytes), "text"

    def _handle_csv(self, file_bytes: bytes) -> Tuple[DataFrame, str]:
        return self.file_reader.read_csv(file_bytes), "df"

    def _handle_xlsx(self, file_bytes: bytes) -> Tuple[DataFrame, str]:
        return self.file_reader.read_xlsx(file_bytes), "df"

    def _handle_json(self, file_bytes: bytes) -> Tuple[List[Dict], str]:
        return [self.file_reader.read_json(file_bytes)], "json"
    

    def ingest(self, file: Union[UploadFile, Path], output_dir: Path = None) -> Tuple[Any, str]:
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
                raise NotImplementedError("Directory ingestion not implemented yet.")
            file_bytes = file.read_bytes()
            ext = file.suffix.lower()
        else: # isinstance(file, UploadFile)
            file_bytes = file.file.read()
            ext = f".{file.filename.split('.')[-1].lower()}"

        handler = self._handler_map.get(ext)
        if not handler:
            raise ValueError(f"Unsupported file type: {ext}")

        return handler(file_bytes)

