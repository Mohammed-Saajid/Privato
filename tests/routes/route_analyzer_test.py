import io
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import MagicMock

from app.main import app  # FastAPI app is initialized in app/main.py
from app.api.routes.analyzer import router

# Include router in app for testing if not already included
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_ingestor():
    return MagicMock()


@pytest.fixture
def mock_analyzer():
    return MagicMock()


@pytest.fixture(autouse=True)
def override_dependencies(mock_ingestor, mock_analyzer):
    app.dependency_overrides = {}
    from app.dependencies import get_ingestor, get_analyzer
    app.dependency_overrides[get_ingestor] = lambda: mock_ingestor
    app.dependency_overrides[get_analyzer] = lambda: mock_analyzer
    yield
    app.dependency_overrides = {}


class TestAnalyzerRoutes:

    def test_analyze_file_image(self, client, mock_ingestor, mock_analyzer):
        mock_ingestor.ingest.return_value = ("fake_image_bytes", "img")
        mock_analyzer.analyze_image.return_value = [{"result": "image_analysis"}]

        response = client.post(
            "/analyzer/upload_file",
            files={"file": ("test.png", io.BytesIO(b"fakeimage"), "image/png")},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["analysis"][0]["result"] == "image_analysis"
        assert data["message"] == "Analysis completed successfully."
        mock_analyzer.analyze_image.assert_called_once_with("fake_image_bytes")

    def test_analyze_file_multiple_images(self, client, mock_ingestor, mock_analyzer):
        mock_ingestor.ingest.return_value = (["img1", "img2"], "imgs")
        mock_analyzer.analyze_image.side_effect = [
            {"result": "img1_analysis"},
            {"result": "img2_analysis"},
        ]

        response = client.post(
            "/analyzer/upload_file",
            files={"file": ("test.zip", io.BytesIO(b"fakezip"), "application/zip")},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["analysis"] == [
            {"result": "img1_analysis"},
            {"result": "img2_analysis"},
        ]

    def test_analyze_file_text(self, client, mock_ingestor, mock_analyzer):
        mock_ingestor.ingest.return_value = ("some text", "text")
        mock_analyzer.analyze_text.return_value = [{"result": "text_analysis"}]

        response = client.post(
            "/analyzer/upload_file",
            files={"file": ("test.txt", io.BytesIO(b"some text"), "text/plain")},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["analysis"] == [{"result": "text_analysis"}]
        mock_analyzer.analyze_text.assert_called_once_with("some text")

    def test_analyze_file_dataframe(self, client, mock_ingestor, mock_analyzer):
        pass

    def test_analyze_file_json(self, client, mock_ingestor, mock_analyzer):
        pass

    def test_analyze_file_internal_error(self, client, mock_ingestor):
        mock_ingestor.ingest.side_effect = Exception("Unexpected error")

        response = client.post(
            "/analyzer/upload_file",
            files={"file": ("test.txt", io.BytesIO(b"content"), "text/plain")},
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Internal Server Error" in response.json()["detail"]
