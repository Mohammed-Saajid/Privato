"""Configuration settings for the app."""
import logging
import sys
from privato.core.logging import InterceptHandler
from loguru import logger

API_PREFIX = "/api"
VERSION = "0.1.2"
DEBUG: bool = False
MEMOIZATION_FLAG: bool = True

PROJECT_NAME: str = "Privato"

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

MODEL_PATH = "privato/ml/model/"
SIGNATURE_MODEL_NAME = "yolov8s.onnx"
SIGNATURE_REPO_ID = "tech4humans/yolov8s-signature-detector"
HUGGING_FACE_KEY = ""
FACE_MODEL_NAME = "model.pt"
FACE_REPO_ID = "arnabdhar/YOLOv8-Face-Detection"
LANGUAGE_CONFIG = "docs/languages-config.yml"
SUPPORTED_LANGUAGES = "en,es,de".split(",")

logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
logging.getLogger("presidio-analyzer").propagate = False