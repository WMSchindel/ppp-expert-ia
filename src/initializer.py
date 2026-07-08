"""
Application initialization with structured logging.

This module is responsible for initializing the application and logging
the startup sequence. It should be called after all modules are loaded
to avoid circular imports.
"""

from src.core.logging import logger
from src.core.version import version
from src.core.config.settings import settings
from src.core.config.defaults import DEFAULT_LOG_LEVEL, DEFAULT_DATABASE_FILENAME
from src.core.config.environments import Environment


def initialize_application() -> None:
    """Initialize the application with proper logging."""
    logger.info("=" * 70)
    logger.info(f"Application: {version.app_name} v{version.version}")
    logger.info(f"Author: {version.author}")
    logger.info("=" * 70)

    logger.info("Environment module loaded")
    logger.debug(f"Available environments: {[e.value for e in Environment]}")

    logger.info("Default configuration loaded")
    logger.debug(f"Default log level: {DEFAULT_LOG_LEVEL}")
    logger.debug(f"Default database: {DEFAULT_DATABASE_FILENAME}")

    logger.info("Settings instance created")
    logger.debug(f"Current environment: {settings.environment}")
    logger.debug(f"Log level: {settings.log_level}")

    logger.info("Project paths initialized")
    logger.debug(f"Project root: {settings.project_root}")
    logger.debug(f"Database directory: {settings.database_directory}")

    logger.info("Application initialization complete")
