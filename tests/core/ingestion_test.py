import io
import pytest
from unittest.mock import MagicMock, patch
from fastapi import UploadFile
from PIL import Image
import pandas as pd
import json

from privato.app.core.ingestion import Ingestor


def make_upload_file(filename: str, content: bytes, content_type: str = "application/octet-stream"):
    """Helper to create an UploadFile-like object with content."""
    file_obj = io.BytesIO(content)
    upload = UploadFile(filename=filename, file=file_obj)
    return upload


@pytest.fixture
def mock_pdf_converter():
    with patch("app.core.ingestion.PDFToImageConverter") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_file_reader():
    with patch("app.core.ingestion.FileReader") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ingestor(mock_pdf_converter, mock_file_reader):
    return Ingestor(dpi=150)


class TestIngestor:

    def test_ingest_pdf(self, ingestor, mock_pdf_converter, mock_file_reader, tmp_path):
        fake_path = tmp_path / "page1.png"
        fake_path.write_bytes(b"fakeimage")
        mock_pdf_converter.convert.return_value = [fake_path]

        img = Image.new("RGB", (5, 5))
        mock_file_reader.read_image.return_value = img

        upload = make_upload_file("doc.pdf", b"fakepdf", "application/pdf")
        result, ext = ingestor.ingest(upload)

        assert ext == "imgs"
        assert isinstance(result, list)
        assert result[0] is img
        mock_pdf_converter.convert.assert_called_once()
        mock_file_reader.read_image.assert_called_once_with(fake_path)

    def test_ingest_image(self, ingestor, mock_file_reader):
        img = Image.new("RGB", (10, 10))
        mock_file_reader.read_image.return_value = img

        upload = make_upload_file("photo.png", b"fakebytes", "image/png")
        result, ext = ingestor.ingest(upload)

        assert ext == "img"
        assert isinstance(result, Image.Image)
        mock_file_reader.read_image.assert_called_once()

    def test_ingest_text(self, ingestor, mock_file_reader):
        mock_file_reader.read_text.return_value = "hello world"

        upload = make_upload_file("note.txt", b"hello world", "text/plain")
        result, ext = ingestor.ingest(upload)

        assert ext == "text"
        assert result == "hello world"
        mock_file_reader.read_text.assert_called_once_with(b"hello world")

    def test_ingest_xlsx(self, ingestor, mock_file_reader):
        df = pd.DataFrame({"a": [1]})
        mock_file_reader.read_xlsx.return_value = df

        upload = make_upload_file("sheet.xlsx", b"fakebytes", "application/vnd.ms-excel")
        result, ext = ingestor.ingest(upload)

        assert ext == "df"
        assert isinstance(result, list)
        assert isinstance(result[0], pd.DataFrame)

    def test_ingest_csv(self, ingestor, mock_file_reader):
        df = pd.DataFrame({"col": [1, 2]})
        mock_file_reader.read_csv.return_value = df

        upload = make_upload_file("data.csv", b"col\n1\n2", "text/csv")
        result, ext = ingestor.ingest(upload)

        assert ext == "df"
        assert isinstance(result[0], pd.DataFrame)

    def test_ingest_json(self, ingestor, mock_file_reader):
        mock_file_reader.read_json.return_value = {"key": "value"}

        upload = make_upload_file("data.json", json.dumps({"key": "value"}).encode(), "application/json")
        result, ext = ingestor.ingest(upload)

        assert ext == "json"
        assert result == [{"key": "value"}]
        mock_file_reader.read_json.assert_called_once()

    def test_ingest_unsupported_type(self, ingestor):
        upload = make_upload_file("archive.zip", b"fake", "application/zip")

        with pytest.raises(ValueError) as exc:
            ingestor.ingest(upload)

        assert "Unsupported file type" in str(exc.value)
