"""Logging configuration using Loguru with an intercept handler for standard logging integration."""
import logging

from loguru import logger

logging.basicConfig(level=logging.INFO)

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

