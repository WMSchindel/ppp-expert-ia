"""
Base Entity class for domain entities with logging support.

All domain entities should inherit from this class to automatically
get logging of creation and operations.
"""

from abc import ABC
from src.core.logging import logger


class Entity(ABC):
    """Base class for all domain entities.

    Provides automatic logging of entity lifecycle:
    - Creation events
    - Validation operations
    - State changes
    """

    def __init__(self, **kwargs):
        """Initialize entity with automatic logging."""
        entity_name = self.__class__.__name__
        logger.info(f"Entity {entity_name} created")
        logger.debug(f"Attributes: {list(kwargs.keys())}")

    def __repr__(self) -> str:
        """String representation for logging."""
        return f"{self.__class__.__name__}({self.__dict__})"
