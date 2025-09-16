"""Core Utilities."""
from pathlib import Path
from PIL import Image
from typing import List
from io import BytesIO
from PIL import Image
import shutil
from fastapi import UploadFile
from contextlib import contextmanager
from pathlib import Path
import tempfile
from typing import Union, Optional,Any, Dict, List
from typing import Generator
import os
def load_image(image_path: str) -> Image.Image:
    """
    Load an image from the specified file path.

    :param image_path: Path to the image file.
    :return: PIL Image object.
    """
    return Image.open(image_path)


@contextmanager
def save_upload_file(upload_file: UploadFile): #-> Generator[Path]:
    """
    """
    try: 
        with tempfile.NamedTemporaryFile(delete=False, suffix=upload_file.filename) as temp_f:
            shutil.copyfileobj(upload_file.file, temp_f)
            temp_f.flush()
            temp_f.close()
            yield Path(temp_f.name)
    finally:
        upload_file.file.close()
        os.remove(temp_f.name)

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

@contextmanager
def text_temp_file(content: str) -> Generator[Path, None, None]:
    """
    A context manager to safely write a string to a temporary file.
    The file is automatically deleted upon exiting the 'with' block.

    :param content: Text content to write.
    :return: A generator yielding the path to the temporary file.
    """
    #  Create a secure temporary file and get its path
    fd, path_str = tempfile.mkstemp(suffix=".txt", text=True)
    path = Path(path_str)

    try:
        #  Write content to the file
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        #  Yield the path for the user to work with
        yield path
    finally:
        #  Guarantee the file is deleted
        os.remove(path)


@contextmanager
def image_temp_file(image: Image.Image, format: str = "PNG") -> Generator[Path, None, None]:
    """
    A context manager to safely save a PIL Image to a temporary file.
    The file is automatically deleted upon exiting the 'with' block.

    :param image: The PIL.Image object to save.
    :param format: The image format (e.g., 'PNG', 'JPEG').
    :return: A generator yielding the path to the temporary image file.
    """
    #  Create a secure temporary file path
    suffix = f".{format.lower()}"
    fd, path_str = tempfile.mkstemp(suffix=suffix)
    os.close(fd) # Close the low-level descriptor; PIL will handle the rest
    path = Path(path_str)
    
    try:
        #  Save the image to the path
        image.save(path, format=format)
        #  Yield the path for the user to work with
        yield path
    finally:
        #  Guarantee the file is deleted
        os.remove(path)


def images_to_pdf(image_paths: List[Path], output_pdf_path: Path) -> Optional[Path]:
    """
    Merge multiple images into a single PDF file in a memory-efficient way.

    :param image_paths: List of paths to image files.

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
        # Optionally re-raise the exception if the caller should handle it
        # raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # raise
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
    """Helper function to check items within a list."""
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