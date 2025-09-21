import io
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import MagicMock
from PIL import Image

from privato.app.api.routes.redactor import router
from privato.app.main import app  # Assuming FastAPI instance is in app/main.py


# Attach router for tests if not already included in app
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_ingestor():
    return MagicMock()


@pytest.fixture
def mock_redactor():
    return MagicMock()


@pytest.fixture(autouse=True)
def override_dependencies(mock_ingestor, mock_redactor):
    app.dependency_overrides = {}
    from privato.app.dependencies import get_ingestor, get_redactor
    app.dependency_overrides[get_ingestor] = lambda: mock_ingestor
    app.dependency_overrides[get_redactor] = lambda: mock_redactor
    yield
    app.dependency_overrides = {}


class TestRedactorRoutes:

    def test_redact_file_image(self, client, mock_ingestor, mock_redactor):
        mock_ingestor.ingest.return_value = ("fake_image", "img")
        mock_redactor.redact_image.return_value = Image.new("RGB", (10, 10))

        response = client.post(
            "/redactor/upload_file",
            files={"file": ("test.png", io.BytesIO(b"fakeimage"), "image/png")},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "image/png"
        mock_redactor.redact_image.assert_called_once_with("fake_image")

    def test_redact_file_text(self, client, mock_ingestor, mock_redactor):
        mock_ingestor.ingest.return_value = ("some text", "text")
        mock_redactor.redact_text.return_value = {"redacted": "*****"}

        response = client.post(
            "/redactor/upload_file",
            files={"file": ("test.txt", io.BytesIO(b"secret text"), "text/plain")},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"redacted": "*****"}
        mock_redactor.redact_text.assert_called_once_with("some text")

    def test_redact_file_multiple_images_pdf_success(self, client, mock_ingestor, mock_redactor):
        mock_ingestor.ingest.return_value = (["img1", "img2"], "imgs")
        mock_redactor.redact_pdf.return_value = b"%PDF-1.4 fake pdf"

        response = client.post(
            "/redactor/upload_file",
            files={"file": ("test.zip", io.BytesIO(b"fakezip"), "application/zip")},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment; filename=redacted_output.pdf" in response.headers["content-disposition"]

    def test_redact_file_multiple_images_pdf_failure(self, client, mock_ingestor, mock_redactor):
        mock_ingestor.ingest.return_value = (["img1", "img2"], "imgs")
        mock_redactor.redact_pdf.return_value = None

        response = client.post(
            "/redactor/upload_file",
            files={"file": ("test.zip", io.BytesIO(b"fakezip"), "application/zip")},
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Failed to create PDF"}

    def test_redact_file_json(self, client, mock_ingestor, mock_redactor):
        pass

    def test_redact_file_dataframe(self, client, mock_ingestor, mock_redactor):
        pass
    def test_redact_file_internal_error(self, client, mock_ingestor):
        mock_ingestor.ingest.side_effect = Exception("Unexpected error")

        response = client.post(
            "/redactor/upload_file",
            files={"file": ("test.txt", io.BytesIO(b"content"), "text/plain")},
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Unexpected error" in response.json()["detail"]
