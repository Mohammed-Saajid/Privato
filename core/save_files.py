"""File saving utilities."""

from pathlib import Path
from typing import Any, List, Union
from PIL import Image
from io import BytesIO
import logging
import json
from pandas import DataFrame


logger = logging.getLogger(__name__)

class SaveFiles:
    def __init__(self, output_path: Union[str, Path]):
        self.output_path = Path(output_path)
        if not self.output_path.exists():
            self.output_path.mkdir(parents=True, exist_ok=True)
        elif not self.output_path.is_dir():
            raise ValueError(f"Output path {self.output_path} is not a directory.")
        logger.info(f"Output directory set to: {self.output_path}")
        self._handler_map = {
            "img": self._save_image,
            "text": self._save_text,
            "imgs": self._save_pdf,
            "json": self._save_json,
            "df": self._save_dataframe
        }
        self._types_map = {
            Image.Image: "img",
            str: "text",
            bytes: "imgs",
            list[Image.Image]: "imgs",
            dict: "json",
            list: "json", # Assuming list of dicts for JSON
            DataFrame: "df"

        }
    def save(self, data: Union[Image.Image, str, bytes], data_type: str, filename: str) -> Path:
        """Save data to a file based on its type.
        Args:
            data (Union[Image.Image, str, bytes]): The data to save.
            data_type (str): The type of the data ('img', 'text', 'json', 'df', 'imgs').
            filename (str): The base filename to use for saving the file (without extension).
        Returns:
            Path: The path to the saved file.
        """
        if data_type not in self._handler_map:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self._handler_map[data_type](data, filename)
    def save_files(self, files: List[Union[Image.Image, str, bytes]], filenames: list[str]) -> list[Path]:
        """Save a list of files based on their types.
        Args:
            files (list[Union[Image.Image, str, bytes]]): The list of files to save.
            filenames (list[str]): The list of base filenames to use for saving the files (without extensions).
        Returns:
            list[Path]: The list of paths to the saved files.
        """
        if len(files) != len(filenames):
            raise ValueError("The number of files and filenames must be the same.")
        saved_paths = []
        for file, filename in zip(files, filenames):
            data_type = self._get_datatype(file)
            if not data_type:
                raise ValueError(f"Could not determine data type for file: {filename}")
            saved_path = self.save(file, data_type=data_type, filename=filename)
            saved_paths.append(saved_path)
        return saved_paths
    def _save_pdf(self, images: Union[List[Image.Image], bytes], filename: str) -> Path:
        if not images:
            raise ValueError("No images provided to save as PDF.")
        output_file = self.output_path / f"{filename}.pdf"
        if isinstance(images, bytes):
            images = [Image.open(BytesIO(images))]
        images[0].save(output_file, save_all=True, append_images=images[1:], format="PDF")
        logger.info(f"PDF saved to: {output_file}")
        return output_file
    
    def _save_image(self, img: Image.Image, filename: str) -> Path:
        output_file = self.output_path / f"{filename}.png"
        img.save(output_file, format="PNG")
        logger.info(f"Image saved to: {output_file}")
        return output_file
    def _save_text(self, text: str, filename: str) -> Path:
        output_file = self.output_path / f"{filename}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        logger.info(f"Text file saved to: {output_file}")
        return output_file
    def _save_json(self, data: dict, filename: str) -> Path:
        output_file = self.output_path / f"{filename}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"JSON file saved to: {output_file}")
        return output_file
    def _save_dataframe(self, df, filename: str) -> Path:
        output_file = self.output_path / f"{filename}.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"DataFrame saved to: {output_file}")
        return output_file
    def _get_datatype(self, file: Any) -> str:
        if isinstance(file,list):
            if file and isinstance(file[0], dict):
                return "json"
            elif file and isinstance(file[0], Image.Image):
                return "imgs"
        return self._types_map.get(type(file))
