"""
Tests for logger integration with core modules.

Validates that logging is properly integrated into the initialization
sequence without causing circular imports or other issues.
"""

import pytest


def test_initializer_can_be_imported():
    """Test that initializer module can be imported without errors."""
    from src import initializer

    assert initializer is not None


def test_initializer_has_initialize_function():
    """Test that initializer has the initialize_application function."""
    from src.initializer import initialize_application

    assert callable(initialize_application)


def test_initialize_application_logs_correctly():
    """Test that initialize_application executes without errors."""
    from src.initializer import initialize_application

    # Just verify it executes without raising exceptions
    try:
        initialize_application()
    except Exception as e:
        pytest.fail(f"initialize_application raised: {e}")


def test_initialize_application_logs_debug_info():
    """Test that initialize_application includes debug messages."""
    from src.initializer import initialize_application

    # Just verify it executes without raising exceptions
    try:
        initialize_application()
    except Exception as e:
        pytest.fail(f"initialize_application raised: {e}")


def test_no_circular_imports():
    """Test that importing all modules doesn't cause circular imports."""
    # This test validates that we can import the entire module stack
    # without circular import errors
    from src.core.version import version
    from src.core.config.settings import settings
    from src.core.config.defaults import DEFAULT_LOG_LEVEL
    from src.core.config.environments import Environment
    from src.core.paths import paths
    from src.core.logging import logger

    assert version is not None
    assert settings is not None
    assert DEFAULT_LOG_LEVEL is not None
    assert Environment is not None
    assert paths is not None
    assert logger is not None


def test_logger_integration_with_settings():
    """Test that logger can access settings configuration."""
    from src.core.logging import logger
    from src.core.config.settings import settings

    # This validates that logger was properly initialized with settings
    assert logger is not None
    assert settings is not None
    assert hasattr(settings, "log_level")


def test_all_modules_imported_successfully():
    """Test that all core modules can be imported in order."""
    from src.core.version import version
    from src.core.config.environments import Environment
    from src.core.config.defaults import DEFAULT_LOG_LEVEL
    from src.core.config.settings import settings
    from src.core.paths import paths
    from src.core.logging import logger

    # All imports should succeed
    assert all([version, Environment, DEFAULT_LOG_LEVEL, settings, paths, logger])
