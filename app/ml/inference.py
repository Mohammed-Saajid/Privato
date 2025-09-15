"""To perform inference on image data using machine learning models."""

import os 
from ultralytics import YOLO
from PIL import Image
from app.core.config import MODEL_PATH, SIGNATURE_MODEL_NAME, FACE_MODEL_NAME, SIGNATURE_REPO_ID, FACE_REPO_ID
from presidio_image_redactor.entities import ImageRecognizerResult
from typing import List, Dict, Any
import json
from ml.pull_models import download_model

class ImageInference:
    """Class to handle image inference using a pre-trained YOLO models."""

    def __init__(self, model_path: str = MODEL_PATH):
        """Initialize the ImageInference class with the model path and name.
        Args:
            model_path (str): The path where the model is stored.
        """
        self.signature_model_name = SIGNATURE_MODEL_NAME
        self.face_model_name = FACE_MODEL_NAME
        # Download models if they are not present
        download_model(model_filename=self.signature_model_name, model_path=model_path, repo_id=SIGNATURE_REPO_ID)
        download_model(model_filename=self.face_model_name, model_path=model_path, repo_id=FACE_REPO_ID)
        self.signature_model_path = os.path.join(model_path, self.signature_model_name)
        self.signature_model = YOLO(self.signature_model_path, task="detect")
        self.face_model_path = os.path.join(model_path, self.face_model_name)
        self.face_model = YOLO(self.face_model_path, task="detect")

    def perform_inference(self, image: Image.Image) -> List[Dict]:
        """Perform inference on the given image and return annotated results.
        Args:
            image (Image): The input image for inference.
        Returns:
            List[Dict]: A list of dictionaries containing detected entities and their details.
        """

        sign_results = self.signature_model(image)[0]
        face_results = self.face_model(image)[0]
        return self._convert_yolo_to_presidio(json.loads(face_results.to_json())) + self._convert_yolo_to_presidio(json.loads(sign_results.to_json()))

    def _convert_yolo_to_presidio(self,yolo_results: Dict[str, Any]) -> List[ImageRecognizerResult]:
        """
        Converts YOLO model detection results to a list of ImageRecognizerResult objects.

        Args:
            yolo_results: A dictionary containing the YOLO model's output, including
                          'boxes', 'scores', and 'labels'.

        Returns:
            A list of ImageRecognizerResult objects.
        """
        presidio_results = []
        num_detections = len(yolo_results)
        
        for i in range(num_detections):
            # Extract data for a single detection
            box = yolo_results[i]['box']
            score = yolo_results[i]['confidence']
            label = yolo_results[i]['name']
            boxes = tuple(box.values())
            x_min, y_min, x_max, y_max = boxes
            # Create the ImageRecognizerResult object
            result = ImageRecognizerResult(
                entity_type=label,
                start=0,
                end=1,
                score=float(score),
                left=int(x_min),
                top=int(y_min),
                width=int(x_max - x_min),
                height=int(y_max - y_min),
            )
            presidio_results.append(result)

        return presidio_results

