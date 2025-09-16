"""Analyzer module for text and image analysis."""
from app.core.image_analyzer_engine import CustomImageAnalyzerEngine as ImageAnalyzerEngine
from PIL import Image
from typing import List,Dict, Optional
from presidio_structured import StructuredEngine, PandasAnalysisBuilder, JsonAnalysisBuilder
from presidio_structured.config import StructuredAnalysis
from app.core.analyzer_engine import CustomAnalyzerEngine as AnalyzerEngine
from app.core.utils import check_json_complexity
class Analyzer:
    """Analyzer class for text and image analysis."""
    def __init__(self):
        """Initialize the Analyzer class.
        Args:
            log_decision_process (bool, optional): Whether to log the decision process. Defaults to False.
        """
        self.analyzer = AnalyzerEngine()
        self.image_analyzer = ImageAnalyzerEngine()
        self.pandas_analyzer = PandasAnalysisBuilder(analyzer=self.analyzer)
        self.json_analyzer = JsonAnalysisBuilder(analyzer=self.analyzer)
        
    def analyze_text(self, text: str, language: str = "en", entities: list = None) -> List[Dict]:
        """Analyze text for sensitive information.
        Args:
            text (str): The text to analyze.
            language (str, optional): The language of the text. Defaults to "en".
            entities (list, optional): List of entity types to look for. Defaults to None.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        results = self.analyzer.analyze(
            text=text,
            entities=entities,
            language=language
        )
        return [result.to_dict() for result in results]

    def analyze_image(self, img: Image, language: str = "en") -> List[Dict]:
        """Analyze image for sensitive information.
        Args:
            img (Image): The image to analyze.
            language (str, optional): The language of the image content. Defaults to "en".
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        results = self.image_analyzer.analyze(
            image=img,
            ocr_kwargs=None,
            language=language
        )

        return [result.to_dict() for result in results]

    def analyze_dataframe(self, df, language: str = "en") -> StructuredAnalysis:
        """Analyze text data within a DataFrame.
        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            language (str): The languageof the data.
        Returns:
            List[Dict]: List of recognized entities with their details.
        """
        tabular_analysis = self.pandas_analyzer.generate_analysis(df=df,language=language)
        return tabular_analysis


    def analyze_json(self, json_data: Dict, language: str = "en") -> StructuredAnalysis:
        """Analyze text data within a JSON object.
        Args:
            json_data (dict): The JSON data to analyze.
            language (str): The language of the data.
        Returns:
            StructuredAnalysis: The structured analysis result.
        """
        check_json_complexity(json_data)
        analysis = self.json_analyzer.generate_analysis(data=json_data, language=language)
        return analysis

