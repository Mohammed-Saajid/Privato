import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import io

from privato.core.analyzer import Analyzer


@pytest.fixture
def analyzer_with_mocks():
    """Provide Analyzer instance with mocked engines."""
    with patch("app.core.analyzer.AnalyzerEngine") as mock_text_engine, \
         patch("app.core.analyzer.ImageAnalyzerEngine") as mock_image_engine:

        mock_text_instance = MagicMock()
        mock_image_instance = MagicMock()

        mock_text_engine.return_value = mock_text_instance
        mock_image_engine.return_value = mock_image_instance

        analyzer = Analyzer()
        analyzer.text_analyzer = mock_text_instance
        analyzer.image_analyzer = mock_image_instance

        yield analyzer, mock_text_instance, mock_image_instance


class TestAnalyzer:

    def test_analyze_text_returns_dicts(self, analyzer_with_mocks):
        analyzer, mock_text_engine, _ = analyzer_with_mocks

        # Mock presidio results with a .to_dict method
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"entity_type": "PERSON", "text": "John"}
        mock_text_engine.analyze.return_value = [mock_result]

        results = analyzer.analyze_text("Hello John")

        assert isinstance(results, list)
        assert results == [{"entity_type": "PERSON", "text": "John"}]
        mock_text_engine.analyze.assert_called_once_with(
            text="Hello John", entities=None, language="en"
        )

    def test_analyze_text_with_entities_and_language(self, analyzer_with_mocks):
        analyzer, mock_text_engine, _ = analyzer_with_mocks
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"entity_type": "EMAIL", "text": "test@example.com"}
        mock_text_engine.analyze.return_value = [mock_result]

        entities = ["EMAIL_ADDRESS"]
        results = analyzer.analyze_text("Contact me at test@example.com", language="en", entities=entities)

        assert results == [{"entity_type": "EMAIL", "text": "test@example.com"}]
        mock_text_engine.analyze.assert_called_once_with(
            text="Contact me at test@example.com", entities=entities, language="en"
        )

    def test_analyze_image_returns_dicts(self, analyzer_with_mocks):
        analyzer, _, mock_image_engine = analyzer_with_mocks

        # Create a dummy in-memory image
        img = Image.new("RGB", (10, 10))
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"entity_type": "FACE", "bbox": [0, 0, 10, 10]}
        mock_image_engine.analyze.return_value = [mock_result]

        results = analyzer.analyze_image(img)

        assert results == [{"entity_type": "FACE", "bbox": [0, 0, 10, 10]}]
        mock_image_engine.analyze.assert_called_once_with(image=img)

    def test_analyze_dataframe_not_implemented(self, analyzer_with_mocks):
        analyzer, _, _ = analyzer_with_mocks
        with pytest.raises(NotImplementedError, match="DataFrame analysis not implemented yet."):
            analyzer.analyze_dataframe("fake_df")

    def test_analyze_json_not_implemented(self, analyzer_with_mocks):
        analyzer, _, _ = analyzer_with_mocks
        with pytest.raises(NotImplementedError, match="JSON analysis not implemented yet."):
            analyzer.analyze_json({"key": "value"})
