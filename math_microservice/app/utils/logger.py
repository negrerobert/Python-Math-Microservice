"""
Logging configuration for the math microservice
"""
import logging
import sys
from typing import Dict, Any
from pythonjsonlogger import jsonlogger
from datetime import datetime


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields"""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        # Add timestamp
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()

        # Add service info
        log_record['service'] = 'math-microservice'
        log_record['level'] = record.levelname

        # Add function and line info for debug logs
        if record.levelno <= logging.DEBUG:
            log_record['function'] = record.funcName
            log_record['line'] = record.lineno


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with JSON formatting

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Set log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Create JSON formatter
    formatter = CustomJsonFormatter(
        fmt='%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


# Application loggers
app_logger = setup_logger("math_microservice.app")
api_logger = setup_logger("math_microservice.api")
cache_logger = setup_logger("math_microservice.cache")
db_logger = setup_logger("math_microservice.database")
performance_logger = setup_logger("math_microservice.performance")