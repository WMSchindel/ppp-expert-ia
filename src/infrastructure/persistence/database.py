"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.core.config.settings import settings
from src.core.logging import logger
from src.infrastructure.persistence.models.usuario_model import Base

# Create engine
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=False,  # SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")


def init_db():
    """Initialize database with all tables."""
    from src.infrastructure.persistence.models.usuario_model import Base

    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
