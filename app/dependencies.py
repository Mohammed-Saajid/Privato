"""Dependency injection functions for the app."""

from core.ingestion import Ingestor
from core.analyzer import Analyzer
from core.redactor import Redactor

# These objects are created once and shared across all requests.
ingestor = Ingestor()
analyzer = Analyzer()
redactor = Redactor()

def get_ingestor() -> Ingestor:
    """
    Dependency function to get the Ingestor instance.
    Args:
        None
    Returns:
        Ingestor: The shared Ingestor instance.
    """
    return ingestor

def get_analyzer() -> Analyzer:
    """
    Dependency function to get the Analyzer instance.
    Args:
        None
    Returns:
        Analyzer: The shared Analyzer instance.
    """
    return analyzer

def get_redactor() -> Redactor:
    """
    Dependency function to get the Redactor instance.
    Args:
        None
    Returns:
        Redactor: The shared Redactor instance.
    """
    return redactor
