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
    def read_text(self, file : bytes) -> str:
        """
        Read text content from a .txt file.
        Args:
            file (bytes): The bytes of the .txt file.
        Returns:
            str: Content of the text file.
        """
        return file.decode('utf-8')
    def read_xlsx(self, file: IO[bytes]) -> str:
        """
        Read content from a .xlsx file and returns a Pandas dataframe.
        Args:
            file (IO[bytes]): The bytes of the .xlsx file.
        Returns:
            DataFrame: Pandas dataframe containing the content of the Excel file.
        """
        return pd.read_excel(BytesIO(file))
    def read_csv(self, file: IO[bytes]) -> DataFrame:
        """
        Read content from a .csv file and returns a Pandas dataframe.
        Args:
            file (IO[bytes]): The bytes of the .csv file.
        Returns:
            DataFrame: Pandas dataframe containing the content of the CSV file.
        """
        return pd.read_csv(BytesIO(file))
    def read_json(self, file: IO[bytes]) -> dict:
        """
        Read Content from a .json file and returns a Dictionary.
        Args:
            file (IO[bytes]): The bytes of the .json file.
        Returns:
            dict: Dictionary containing the content of the JSON file.
        """
        return json.loads(file)

    def read_image(self, file: Union[IO[bytes],Path]) -> Image.Image:
        """
        Read an image from the specified file path.
        Args:
            file Union[IO[bytes],Path]: The path to the image file or bytes of the image file.
        Returns:
            Image.Image: The loaded image object.
        """
        if isinstance(file, Path):
            return Image.open(file).convert("RGB")
        return Image.open(BytesIO(file)).convert("RGB")
