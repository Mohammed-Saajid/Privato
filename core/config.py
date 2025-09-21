"""Configuration settings for the app."""
import logging
import sys
from core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret
config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.2"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MEMOIZATION_FLAG: bool = config("MEMOIZATION_FLAG", cast=bool, default=True)

PROJECT_NAME: str = config("PROJECT_NAME", default="Privato")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

MODEL_PATH = config("MODEL_PATH", default="./ml/model/")
SIGNATURE_MODEL_NAME = config("SIGNATURE_MODEL_NAME", default="yolov8s.onnx")
SIGNATURE_REPO_ID = config("SIGNATURE_REPO_ID",default="")
HUGGING_FACE_KEY = config("HF_KEY", cast=Secret, default="")
FACE_MODEL_NAME = config("FACE_MODEL_NAME", default="model.pt")
FACE_REPO_ID = config("FACE_REPO_ID",default="")
LANGUAGE_CONFIG = config("LANGUAGE_CONFIG", default="docs/languages-config.yml")
SUPPORTED_LANGUAGES = config("SUPPORTED_LANGUAGES", default="en,es,de").split(",")

logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)
logging.getLogger("presidio-analyzer").propagate = False