"""Custom Image Analyzer Engine integrating ML model with Presidio."""
from presidio_image_redactor import ImageAnalyzerEngine
from privato.ml.inference import ImageInference
from typing import List, Dict, Any, Optional
from presidio_image_redactor.entities import ImageRecognizerResult
from privato.core.analyzer_engine import CustomAnalyzerEngine as AnalyzerEngine
class CustomImageAnalyzerEngine():
    def __init__(self):
        super().__init__()
        self.image_inference = ImageInference()
        self.analyzer_engine = AnalyzerEngine()
        self.image_analyzer_engine = ImageAnalyzerEngine(
            analyzer_engine=self.analyzer_engine
        )

    def analyze(self, image, ocr_kwargs: Optional[dict] = None, **text_analyzer_kwargs) -> List[ImageRecognizerResult]:
        """Analyze the given image for sensitive information.

        Args:
            image (PIL.Image): The image to analyze.
        Returns:
            List[Dict]: A list of recognized entities with their details.
        """
        results = self.image_inference.perform_inference(image)
        image_analyzer_results = self.image_analyzer_engine.analyze(image=image, ocr_kwargs=ocr_kwargs, **text_analyzer_kwargs)
        results.extend(image_analyzer_results)
        return results

