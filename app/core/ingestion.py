"""Module for ingesting and normalizing various file types."""
from typing import List, Union, Dict, Tuple
from PIL import Image
from pandas import DataFrame
from fastapi import UploadFile, File
from .converter import PDFToImageConverter
from .file_reader import FileReader



class Ingestor:
    """
    Handles ingestion of PDFs, images, or text into a consistent format.
    Converts PDFs to images, reads images, text files, Excel, CSV, and JSON files.
    Attributes:
        SUPPORTED_IMAGE_FORMATS (set): Supported image file extensions.
        SUPPORTED_FILE_FORMATS (set): Supported file extensions for ingestion.
        pdf_to_image (PDFToImageConverter): Instance to convert PDFs to images.
        file_reader (FileReader): Instance to read various file types.     
    """

    
    def __init__(self, dpi: int = 200):
        """Initialize the Ingestor with supported formats and converters.
        Args:
            dpi (int, optional): DPI for PDF to image conversion. Defaults to 200.
        Returns:
            None
        """
        self.SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
        self.SUPPORTED_FILE_FORMATS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".txt", ".xlsx", ".csv", ".json"}
        self.pdf_to_image = PDFToImageConverter(dpi=dpi)
        self.file_reader = FileReader()

    def ingest(self, file: UploadFile = File(...)) -> Union[Tuple[List[Image.Image],str],Tuple[Image.Image,str], Tuple[DataFrame,str], Tuple[str,str], Tuple[Dict,str]]:
        """
        Ingest a document and normalize into images.
        Args:
            file (UploadFile): The uploaded file to ingest.
        Returns:
            Union[Tuple[List[Image.Image],str], Tuple[Image.Image,str], Tuple[DataFrame,str], Tuple[str,str], Tuple[Dict,str]]: A tuple containing the ingested content and its type.
        """
        ext = f".{file.filename.split('.')[-1].lower()}"
        if ext not in self.SUPPORTED_FILE_FORMATS:
            raise ValueError(f"Unsupported file type: {file.content_type}")
        file_bytes = file.file.read()
        if ext == '.pdf':
            image_paths = self.pdf_to_image.convert(file_bytes)
            return [self.file_reader.read_image(img_path) for img_path in image_paths if img_path.exists()], "imgs"
        elif ext in self.SUPPORTED_IMAGE_FORMATS:
            return self.file_reader.read_image(file_bytes),"img"
        elif ext == '.txt':
            return self.file_reader.read_text(file_bytes),"text"
        elif ext == '.xlsx':
            return self.file_reader.read_xlsx(file_bytes),"df"
        elif ext == '.csv':
            return self.file_reader.read_csv(file_bytes),"df"
        elif ext == '.json':
            return self.file_reader.read_json(file_bytes),"json"
