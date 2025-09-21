import io
import os
import pytest
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas

from privato.app.core.converter import PDFToImageConverter


@pytest.fixture
def sample_pdf_bytes():
    """Generate a simple in-memory PDF file with 2 pages."""
    pdf_bytes = io.BytesIO()
    c = canvas.Canvas(pdf_bytes)
    c.drawString(100, 750, "Page 1 - Hello PDF")
    c.showPage()
    c.drawString(100, 750, "Page 2 - Another page")
    c.save()
    return pdf_bytes.getvalue()


class TestPDFToImageConverter:

    def test_convert_single_pdf(self, sample_pdf_bytes):
        """Ensure a PDF is converted into PNG images."""
        converter = PDFToImageConverter(dpi=100)
        output_files = converter.convert(sample_pdf_bytes)

        # Two pages should generate two images
        assert len(output_files) == 2
        for path in output_files:
            assert Path(path).exists()
            img = Image.open(path)
            assert img.format == "PNG"
            img.close()
            os.remove(path)  # cleanup

    def test_output_files_are_different(self, sample_pdf_bytes):
        """Ensure each page of the PDF produces a distinct output file."""
        converter = PDFToImageConverter()
        output_files = converter.convert(sample_pdf_bytes)

        # Ensure file paths are unique
        assert len(set(output_files)) == len(output_files)

        for path in output_files:
            os.remove(path)

    def test_dpi_affects_output_resolution(self, sample_pdf_bytes):
        """Higher DPI should result in larger image dimensions."""
        low_dpi_converter = PDFToImageConverter(dpi=50)
        high_dpi_converter = PDFToImageConverter(dpi=200)

        low_res_images = low_dpi_converter.convert(sample_pdf_bytes)
        high_res_images = high_dpi_converter.convert(sample_pdf_bytes)

        low_img = Image.open(low_res_images[0])
        high_img = Image.open(high_res_images[0])

        assert high_img.width > low_img.width
        assert high_img.height > low_img.height

        low_img.close()
        high_img.close()

        for path in low_res_images + high_res_images:
            os.remove(path)

    def test_invalid_pdf_raises(self):
        """Passing non-PDF data should raise an error."""
        converter = PDFToImageConverter()
        with pytest.raises(Exception):
            converter.convert(b"not a valid pdf")

    def test_empty_pdf_raises(self):
        """An empty PDF should raise an error during conversion."""
        converter = PDFToImageConverter()
        with pytest.raises(Exception):
            converter.convert(b"")
