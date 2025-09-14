"""Module for redacting sensitive information from text and images."""
from presidio_image_redactor import ImageRedactorEngine
from app.core.image_analyzer_engine import CustomImageAnalyzerEngine as ImageAnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from PIL import Image
from presidio_analyzer import AnalyzerEngine
from typing import Dict, List
import json
from pathlib import Path
from pandas import DataFrame
import tempfile
from app.core.utils import images_to_pdf

class Redactor():
    """Redactor class for text and image redaction.
    Attributes:
        image_redactor (ImageRedactorEngine): Instance of the image redactor engine.
        analyzer_engine (AnalyzerEngine): Instance of the text analyzer engine.
        text_anonymyzer (AnonymizerEngine): Instance of the text anonymizer engine.
    """
    def __init__(self, log_decision_process: bool = False):
        """Initialize the Redactor class."""
        self.image_redactor = ImageRedactorEngine(image_analyzer_engine=ImageAnalyzerEngine())
        self.analyzer_engine = AnalyzerEngine(log_decision_process=log_decision_process)
        self.text_anonymyzer = AnonymizerEngine()

    def redact_image(self, img: Image.Image) -> Image.Image:
        """Redact sensitive information from an image.
        Args:
            img (Image): The image to redact.
        Returns:
            Image: The redacted image.
        """
        redacted_image = self.image_redactor.redact(image=img)
        return redacted_image
    
    def redact_text(self, text: str) -> Dict:
        """Redact sensitive information from text.
        Args:
            text (str): The text to redact.
        Returns:
            Dict: The redacted text in JSON format.
        """
        analyzed_text = self.analyzer_engine.analyze(text=text, language="en")
        anonymized_text = self.text_anonymyzer.anonymize(text=text, analyzer_results=analyzed_text)
        return json.loads(anonymized_text.to_json())
    
    def redact_pdf(self, images : List[Image.Image]) -> bytes:
        with tempfile.TemporaryDirectory() as temp_dir:
               temp_dir_path = Path(temp_dir)
               redacted_img_paths = []
               for i, img in enumerate(images, start=1):
                   redacted_img = self.image_redactor.redact(img)
                   temp_img_path = temp_dir_path / f"redacted_page_{i}.png"
                   redacted_img.save(temp_img_path)
                   redacted_img_paths.append(temp_img_path)
               output_pdf_path = temp_dir_path / "redacted_output.pdf"
               output_pdf_path = images_to_pdf(redacted_img_paths, output_pdf_path)
               return output_pdf_path.read_bytes()
        
    
    def redact_json(self, json_data: Dict) -> Dict:
        """Redact sensitive information from JSON data.
        Args:
            json_data (Dict): The JSON data to redact.
        Returns:
            Dict: The redacted JSON data.
        """
        # To be Implemented
        raise NotImplementedError("JSON redaction not implemented yet.")
    
    def redact_df(self, df: DataFrame) -> DataFrame:
        """Redact sensitive information from a DataFrame.
        Args:
            df (DataFrame): The DataFrame to redact.
        Returns:
            DataFrame: The redacted DataFrame.
        """
        # To be implemented
        raise NotImplementedError("DataFrame redaction not implemented yet.")
