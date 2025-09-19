"""File reading utilities for various file formats."""
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import json
from PIL import Image
from typing import IO, Union
from io import BytesIO

class FileReader:
    """
    Utility class to read various file formats.
    """
    def read_text(self, file : Union[bytes, Path]) -> str:
        """
        Read text content from a .txt file.
        Args:
            file (Union[bytes, Path]): The bytes of the .txt file or the file path.
        Returns:
            str: Content of the text file.
        """
        if isinstance(file, Path):
            with open(file, 'r', encoding='utf-8') as f:
                return f.read()
        return file.decode('utf-8')
    def read_xlsx(self, file: Union[bytes, Path]) -> str:
        """
        Read content from a .xlsx file and returns a Pandas dataframe.
        Args:
            file (Union[bytes, Path]): The bytes of the .xlsx file or the file path.
        Returns:
            DataFrame: Pandas dataframe containing the content of the Excel file.
        """
        if isinstance(file, Path):
            return pd.read_excel(file)
        return pd.read_excel(BytesIO(file))
    def read_csv(self, file: Union[bytes, Path]) -> DataFrame:
        """
        Read content from a .csv file and returns a Pandas dataframe.
        Args:
            file (Union[bytes, Path]): The bytes of the .csv file or the file path.
        Returns:
            DataFrame: Pandas dataframe containing the content of the CSV file.
        """
        if isinstance(file, Path):
            return pd.read_csv(file)
        return pd.read_csv(BytesIO(file))
    def read_json(self, file: Union[bytes, Path]) -> dict:
        """
        Read Content from a .json file and returns a Dictionary.
        Args:
            file (Union[bytes, Path]): The bytes of the .json file or the file path.
        Returns:
            dict: Dictionary containing the content of the JSON file.
        """
        if isinstance(file, Path):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return json.loads(file)

    def read_image(self, file: Union[bytes, Path]) -> Image.Image:
        """
        Read an image from the specified file path.
        Args:
            file (Union[bytes, Path]): The path to the image file or bytes of the image file.
        Returns:
            Image.Image: The loaded image object.
        """
        if isinstance(file, Path):
            return Image.open(file).convert("RGB")
        return Image.open(BytesIO(file)).convert("RGB")
