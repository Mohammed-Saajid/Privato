"""Custom Image Analyzer Engine integrating ML model with Presidio."""
from presidio_image_redactor import ImageAnalyzerEngine
from app.ml.inference import ImageInference
from typing import List, Dict, Any, Optional
from presidio_image_redactor.entities import ImageRecognizerResult

class CustomImageAnalyzerEngine():
    def __init__(self):
        super().__init__()
        self.image_inference = ImageInference()
        self.image_analyzer_engine = ImageAnalyzerEngine()

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

