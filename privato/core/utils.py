"""Core Utilities."""
from pathlib import Path
from PIL import Image
from typing import List
from io import BytesIO
from PIL import Image
from pathlib import Path
from typing import Union, Optional,Any, Dict, List
from privato.core.ingestion import Ingestor

def load_image(image_path: str) -> Image.Image:
    """
    Load an image from the specified file path.

    :param image_path: Path to the image file.
    :return: PIL Image object.
    """
    return Image.open(image_path)

def save_img_to_buffer(image: Image.Image, format: str = "PNG") -> BytesIO:
    """
    Save a PIL Image to a bytes buffer.

    :param image: PIL Image object.
    :param format: Format to save the image in (default is PNG).
    :return: Bytes of the saved image.
    """
    buffer = BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer



def images_to_pdf(image_paths: List[Path], output_pdf_path: Path) -> Optional[Path]:
    """
    Merge multiple images into a single PDF file in a memory-efficient way.
    Args:
        image_paths (List[Path]): List of paths to the image files.
        output_pdf_path (Path): Path where the output PDF will be saved.
    Returns:
        Optional[Path]: The path to the saved PDF file, or None if no images were provided.
    """
    if not image_paths:
        print("Warning: No image paths provided.")
        return None

    first_image = None
    try:
        # Open the first image separately
        first_image = Image.open(image_paths[0]).convert("RGB")

        # Create a memory-efficient generator for the rest of the images
        # This opens each image only when it's needed by the save() method.
        remaining_images_iterator = (
            Image.open(path).convert("RGB") for path in image_paths[1:]
        )

        # Save the first image, appending the rest from the generator
        first_image.save(
            output_pdf_path,
            save_all=True,
            append_images=remaining_images_iterator
        )
    except FileNotFoundError as e:
        print(f"Error: Could not find image file at {e.filename}")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e
    finally:
        # Ensure the first image's file handle is always closed
        if first_image:
            first_image.close()
        return output_pdf_path
        
        # Note: The images opened in the generator are automatically handled
        # and closed as they are consumed by the .save() method.
    

def check_json_complexity(data: Dict[str, Any]) -> None:
    """
    Recursively checks a dictionary to see if it contains a list of dictionaries.

    This is used to identify complex JSON structures that are not supported
    by the `JsonAnalysisBuilder` and require manual analysis definition.

    Args:
        data: The dictionary (JSON object) to check.

    Raises:
        NotImplementedError: If a list containing a dictionary is found.
    """
    for value in data.values():
        if isinstance(value, dict):
            # If the value is another dictionary, recurse into it
            check_json_complexity(value)
        elif isinstance(value, list):
            # If the value is a list, check its items
            _check_list_items(value)

def _check_list_items(items: List[Any]) -> None:
    """Helper function to check items within a list.
    Args:
        items (List[Any]): The list of items to check.
    Raises:
        NotImplementedError: If a list containing a dictionary is found.
    Returns:
        None
    """
    for item in items:
        if isinstance(item, dict):
            # This is the "complex" case: a dictionary inside a list
            raise NotImplementedError(
                "Handling JSON with nested objects (dictionaries) in lists is not supported. "
                "Please define the analysis manually using StructuredAnalysis."
            )
        elif isinstance(item, list):
            # Recurse in case of nested lists (e.g., list of lists)
            _check_list_items(item)

def get_dir_files_names(dir_path: Path) -> List[str]:
    """Get a list of file names in a directory.
    Args:
        dir_path (Path): The directory path.
    Returns:
        List[str]: List of file names in the directory.
    """
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Provided path is not a directory: {dir_path}")
    return [file.name for file in dir_path.iterdir() if file.is_file() and file.suffix in Ingestor.SUPPORTED_FILE_FORMATS]