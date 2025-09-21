"""Module to pull models from Hugging Face Hub."""
from privato.core.config import HUGGING_FACE_KEY
from huggingface_hub import login, hf_hub_download
import os

if HUGGING_FACE_KEY:
    login(token=str(HUGGING_FACE_KEY))
else:
    print("Hugging Face key not found. Please set the HF_KEY environment variable.")
    raise ValueError("Hugging Face key not found.")

def download_model(repo_id: str, model_filename: str, model_path: str):
    """Download the model from Hugging Face Hub if not already present.
    Args:
        repo_id (str): The repository ID on Hugging Face Hub.
        model_filename (str): The name of the model file to download.
        model_path (str): The local directory to save the model.
    Returns:
        str: The path to the downloaded model file.
    """
    
    model_file_path = os.path.join(model_path, model_filename)
    
    if not os.path.isfile(model_file_path):
        print(f"Downloading model {model_filename} from repo {repo_id}...")
        hf_hub_download(repo_id=repo_id, filename=model_filename, local_dir=model_path)
        print(f"Model downloaded and saved to {model_file_path}.")
    else:
        print(f"Model {model_filename} already exists at {model_file_path}.")
    
    return model_file_path

