from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from core.config import SUPPORTED_LANGUAGES, LANGUAGE_CONFIG

class CustomAnalyzerEngine:
    """
    A custom wrapper around the Presidio AnalyzerEngine.
    
    This class handles the setup of a multi-lingual engine and can be
    extended with more custom methods in the future.
    """
    def __init__(self, language_conf: str = LANGUAGE_CONFIG):
        """Initializes the engine.
        Args:
            language_conf (str): Path to the language configuration file.
        """
        provider = NlpEngineProvider(conf_file=language_conf)
        self._analyzer_engine = AnalyzerEngine(
            nlp_engine=provider.create_engine(),
            supported_languages=SUPPORTED_LANGUAGES
        )

    def analyze(self, *args, **kwargs):
        """
        Runs the analysis by delegating the call to the underlying engine.
        Args:
            *args: Positional arguments for the analyze method.
            **kwargs: Keyword arguments for the analyze method.
        """
        return self._analyzer_engine.analyze(*args, **kwargs)

