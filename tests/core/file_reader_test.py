import io
import json
import pytest
import pandas as pd
from pathlib import Path
from pandas import DataFrame
from PIL import Image

from app.core.file_reader import FileReader


@pytest.fixture
def file_reader():
    return FileReader()


@pytest.fixture
def sample_csv_bytes():
    return b"col1,col2\n1,2\n3,4"


@pytest.fixture
def sample_xlsx_bytes(tmp_path):
    """Generate an Excel file and return its bytes."""
    df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)

    with open(file_path, "rb") as f:
        return f.read()


@pytest.fixture
def sample_json_bytes():
    return json.dumps({"key": "value"}).encode("utf-8")


@pytest.fixture
def sample_text_bytes():
    return b"Hello, world!"


@pytest.fixture
def sample_image_bytes(tmp_path):
    """Generate a small image and return its bytes."""
    img = Image.new("RGB", (10, 10), color="red")
    file_path = tmp_path / "test.png"
    img.save(file_path, format="PNG")

    with open(file_path, "rb") as f:
        return f.read(), file_path


class TestFileReader:

    def test_read_text(self, file_reader, sample_text_bytes):
        result = file_reader.read_text(sample_text_bytes)
        assert result == "Hello, world!"
        assert isinstance(result, str)

    def test_read_csv(self, file_reader, sample_csv_bytes):
        df = file_reader.read_csv(sample_csv_bytes)
        assert isinstance(df, DataFrame)
        assert df.shape == (2, 2)
        assert list(df.columns) == ["col1", "col2"]

    def test_read_xlsx(self, file_reader, sample_xlsx_bytes):
        df = file_reader.read_xlsx(sample_xlsx_bytes)
        assert isinstance(df, DataFrame)
        assert df.shape == (2, 2)
        assert list(df.columns) == ["col1", "col2"]

    def test_read_json(self, file_reader, sample_json_bytes):
        data = file_reader.read_json(sample_json_bytes)
        assert isinstance(data, dict)
        assert data == {"key": "value"}

    def test_read_json_invalid(self, file_reader):
        with pytest.raises(json.JSONDecodeError):
            file_reader.read_json(b"not a json")

    def test_read_image_from_bytes(self, file_reader, sample_image_bytes):
        img_bytes, _ = sample_image_bytes
        img = file_reader.read_image(img_bytes)
        assert isinstance(img, Image.Image)
        assert img.mode == "RGB"
        assert img.size == (10, 10)

    def test_read_image_from_path(self, file_reader, sample_image_bytes):
        _, file_path = sample_image_bytes
        img = file_reader.read_image(file_path)
        assert isinstance(img, Image.Image)
        assert img.mode == "RGB"
        assert img.size == (10, 10)

    def test_read_image_invalid_bytes(self, file_reader):
        with pytest.raises(Exception):
            file_reader.read_image(b"not an image")
