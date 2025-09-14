"""Analyzer module for text and image analysis."""
from presidio_analyzer import AnalyzerEngine
from app.core.image_analyzer_engine import CustomImageAnalyzerEngine as ImageAnalyzerEngine
from PIL import Image
from typing import List,Dict

class Analyzer:
    """Analyzer class for text and image analysis."""
    def __init__(self,log_decision_process: bool = False):
        """Initialize the Analyzer class.
        Args:
            log_decision_process (bool, optional): Whether to log the decision process. Defaults to False.
        """
        self.text_analyzer = AnalyzerEngine(log_decision_process=log_decision_process)
        self.image_analyzer = ImageAnalyzerEngine()

    def analyze_text(self, text: str, language: str = "en", entities: list = None) -> List[Dict]:
        """Analyze text for sensitive information.
        Args:
            text (str): The text to analyze.
            language (str, optional): The language of the text. Defaults to "en".
            entities (list, optional): List of entity types to look for. Defaults to None.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        results = self.text_analyzer.analyze(
            text=text,
            entities=entities,
            language=language
        )
        return [result.to_dict() for result in results]

    def analyze_image(self, img: Image) -> List[Dict]:
        """Analyze image for sensitive information.
        Args:
            img (Image): The image to analyze.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        results = self.image_analyzer.analyze(
            image=img
        )

        return [result.to_dict() for result in results]
    
    def analyze_dataframe(self, df):
        """Analyze text data within a DataFrame.
        Args:
            df (pd.DataFrame): The DataFrame to analyze.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        # To be implemented: Analyze text data within a DataFrame
        raise NotImplementedError("DataFrame analysis not implemented yet.")

    def analyze_json(self, json_data: Dict):
        """Analyze text data within a JSON object.
        Args:
            json_data (dict): The JSON data to analyze.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        # To be implemented
        raise NotImplementedError("JSON analysis not implemented yet.")
