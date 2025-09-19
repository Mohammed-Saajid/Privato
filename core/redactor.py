"""Module for redacting sensitive information from text and images."""
from presidio_image_redactor import ImageRedactorEngine
from core.image_analyzer_engine import CustomImageAnalyzerEngine as ImageAnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from PIL import Image
from core.analyzer_engine import CustomAnalyzerEngine as AnalyzerEngine
from typing import Any, Dict, List, Union
import json
from pathlib import Path
from pandas import DataFrame
import tempfile
from core.utils import images_to_pdf

class Redactor():
    """Redactor class for text and image redaction.
    Attributes:
        image_redactor (ImageRedactorEngine): Instance of the image redactor engine.
        analyzer_engine (AnalyzerEngine): Instance of the text analyzer engine.
        text_anonymyzer (AnonymizerEngine): Instance of the text anonymizer engine.
    """
    def __init__(self):
        """Initialize the Redactor class."""
        self.image_redactor = ImageRedactorEngine(image_analyzer_engine=ImageAnalyzerEngine())
        self.analyzer_engine = AnalyzerEngine()
        self.text_anonymyzer = AnonymizerEngine()
        self._handler_map : Dict[str, callable] = {
            "img": self.redact_image,
            "text": self.redact_text,
            "imgs": self.redact_pdf,
            "json": self.redact_json,
            "df": self.redact_df
        }
    def redact(self, data: Union[Image.Image, str, List[Image.Image], Dict, DataFrame], data_type: str, language: str = "en") -> Union[Image.Image, Dict, bytes, DataFrame]:
        """Redact sensitive information from the given data based on its type.
        Args:
            data (Union[Image.Image, str, List[Image.Image], Dict, DataFrame]): The data to redact.
            data_type (str): The type of the data ('img', 'text', 'json', 'df').
            language (str, optional): The language of the content. Defaults to "en".
        Returns:
            Any: The redacted data.
        """
        if data_type not in self._handler_map:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self._handler_map[data_type](data, language=language)
    

    def redact_image(self, img: Image.Image, language: str = "en") -> Image.Image:
        """Redact sensitive information from an image.
        Args:
            img (Image): The image to redact.
            language (str, optional): The language of the image content. Defaults to "en".
        Returns:
            Image: The redacted image.
        """
        redacted_image = self.image_redactor.redact(image=img,language=language)
        return redacted_image
    
    def redact_text(self, text: str, language: str = "en") -> Dict:
        """Redact sensitive information from text.
        Args:
            text (str): The text to redact.
            language (str, optional): The language of the text. Defaults to "en".
        Returns:
            Dict: The redacted text in JSON format.
        """
        analyzed_text = self.analyzer_engine.analyze(text=text, language=language)
        anonymized_text = self.text_anonymyzer.anonymize(text=text, analyzer_results=analyzed_text)
        return json.loads(anonymized_text.to_json())

    def redact_pdf(self, images : List[Image.Image], language: str = "en") -> bytes:
        """Redact sensitive information from a list of images (PDF pages).
        Args:
            images (List[Image.Image]): The list of images to redact.
            language (str, optional): The language of the image content. Defaults to "en".
        """
        with tempfile.TemporaryDirectory() as temp_dir:
               temp_dir_path = Path(temp_dir)
               redacted_img_paths = []
               for i, img in enumerate(images, start=1):
                   redacted_img = self.image_redactor.redact(img, language=language)
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
