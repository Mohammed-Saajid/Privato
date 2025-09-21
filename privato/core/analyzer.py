"""Analyzer module for text and image analysis."""
from pandas import DataFrame
from privato.core.image_analyzer_engine import CustomImageAnalyzerEngine as ImageAnalyzerEngine
from PIL import Image
from typing import Any, List,Dict, Optional, Tuple, Union
from presidio_structured import  PandasAnalysisBuilder, JsonAnalysisBuilder
from presidio_structured.config import StructuredAnalysis
from privato.core.analyzer_engine import CustomAnalyzerEngine as AnalyzerEngine
from privato.core.utils import check_json_complexity
from dataclasses import asdict


class Analyzer:
    """Analyzer class for text and image analysis."""
    def __init__(self):
        """
        Initialize the Analyzer class.
        Initializes the underlying analysis engines and sets up a handler map for different data types.
        """
        self.analyzer = AnalyzerEngine()
        self.image_analyzer = ImageAnalyzerEngine()
        self.pandas_analyzer = PandasAnalysisBuilder(analyzer=self.analyzer._analyzer_engine)
        self.json_analyzer = JsonAnalysisBuilder(analyzer=self.analyzer._analyzer_engine)
        self._handler_map : Dict[str, callable] = {
            "img": self.analyze_image,
            "imgs": self.analyze_images,
            "text": self.analyze_text,
            "df": self.analyze_dataframe,
            "json": self.analyze_json
        }
    def analyze(self, data: Any, data_type: str, language: str = "en", entities: list = None) -> Union[List[Dict], Dict]:
        """Analyze the given data based on its type.
        Args:
            data (Any): The data to analyze.
            data_type (str): The type of the data ('img', 'text', 'json', 'df').
            language (str, optional): The language of the content. Defaults to "en".
            entities (list, optional): List of entity types to look for. Defaults to None.
        Returns:
            Union[List[Dict], Dict]: The analysis result.
        """
        if data_type not in self._handler_map:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self._handler_map[data_type](data, language=language, entities=entities)
    
    def analyze_files(self, files: List[Tuple[Union[str,Image.Image, DataFrame, Dict],Any]], language: str = "en", entities: list = None) -> List[Union[List[Dict], Dict]]:
        """Analyze a list of files based on their type.
        Args:
            files (List[Tuple[Union[str, Image.Image, pd.DataFrame, dict], Any]]): The list of files to analyze.
            data_type (str): The type of the data ('img', 'text', 'json', 'df').
            language (str, optional): The language of the content. Defaults to "en".
            entities (list, optional): List of entity types to look for. Defaults to None.
        Returns:
            List[Union[List[Dict], Dict]]: The list of analysis results.
        """
        return [self.analyze(file, data_type=ext, language=language, entities=entities) for file, ext in files]

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

    def analyze_image(self, img: Image.Image, language: str = "en", **kwargs) -> List[Dict]:
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

    def analyze_images(self, images: List[Image.Image], language: str = "en", **kwargs) -> List[List[Dict]]:
        """Analyze a list of images for sensitive information.
        Args:
            images (List[Image.Image]): The list of images to analyze.
            language (str, optional): The language of the image content. Defaults to "en".
        Returns:
            List[List[Dict]]: A list where each element is the analysis result for an image.
        """
        return [self.analyze_image(img, language=language) for img in images]
    

    def analyze_dataframe(self, df: DataFrame, language: str = "en", **kwargs) -> Dict:
        """Analyze text data within a DataFrame.
        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            language (str): The language of the data.
        Returns:
            Dict: The structured analysis result.
        """
        tabular_analysis = self.pandas_analyzer.generate_analysis(df=df,language=language)
        return asdict(tabular_analysis)


    def analyze_json(self, json_data: Dict, language: str = "en", **kwargs) -> Dict:
        """Analyze text data within a JSON object.
        Args:
            json_data (dict): The JSON data to analyze.
            language (str): The language of the data.
        Returns:
            Dict: The structured analysis result.
        """
        check_json_complexity(json_data)
        analysis = self.json_analyzer.generate_analysis(data=json_data, language=language)
        return asdict(analysis)

