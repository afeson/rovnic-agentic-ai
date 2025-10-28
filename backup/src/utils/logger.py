"""
Centralized logging configuration for Rovnic Agentic AI.
"""

import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


def setup_logging(name: str = "rovnic_agentic_ai") -> logging.Logger:
    """Configure logging for the application."""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("Logging initialized")
    return logger


class LoggerMixin:
    """Mixin class to add logging to any class."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get or create logger for this class."""
        name = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return logging.getLogger(name)
