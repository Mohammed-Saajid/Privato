"""PDF to Image Converter Module."""
import os
from pathlib import Path
from typing import List, IO
import fitz
from PIL import Image
import tempfile
from io import BytesIO

class PDFToImageConverter:
    """
    Convert PDF pages to images using PyMuPDF and PIL.
    Each page is converted to a PNG image and saved as a temporary file.
    Args:
        dpi (int): Dots per inch for the output images. Default is 200.
    Returns:
        List[Path]: List of paths to the generated image files.
    """
    def __init__(self, dpi=200):
        self.dpi = dpi
    def convert(self, file: IO[bytes]) -> List[Path]:
        """
        Convert a PDF file to a list of PNG images.
        Args:
            file (IO[bytes]): The bytes of the input PDF file.
        Returns:
            List[Path]: List of paths to the generated PNG image files.
        """
        output_files = []

        with fitz.open(stream=BytesIO(file), filetype="pdf") as pdf:
            for page_num, page in enumerate(pdf,start=1):
                pix = page.get_pixmap(dpi = self.dpi)
                img =  Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                fd, temp_path = tempfile.mkstemp(suffix=f"_page{page_num}.png")
                os.close(fd)
                output_path = Path(temp_path)
                img.save(output_path, format="PNG")
                img.close()
                output_files.append(output_path)
        return output_files
