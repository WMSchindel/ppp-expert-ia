"""
Testes unitários do módulo defaults.py.
"""

from core.config.defaults import (
    DEFAULT_DATABASE_FILENAME,
    DEFAULT_ENCODING,
    DEFAULT_LANGUAGE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_OUTPUT_DIRECTORY,
    DEFAULT_TIMEZONE,
    DEFAULT_WORD_TEMPLATE,
    GIGABYTE,
    KILOBYTE,
    MAX_UPLOAD_SIZE,
    MEGABYTE,
    DEFAULT_ENVIRONMENT,
)


def test_storage_units():
    """Verifica as unidades de medida."""

    assert KILOBYTE == 1024
    assert MEGABYTE == 1024 * KILOBYTE
    assert GIGABYTE == 1024 * MEGABYTE


def test_default_environment():
    """Verifica o ambiente padrão."""

    from core.config.environments import Environment

    assert DEFAULT_ENVIRONMENT == Environment.DEVELOPMENT


def test_default_general_settings():
    """Verifica as configurações gerais."""

    assert DEFAULT_LANGUAGE == "pt-BR"
    assert DEFAULT_ENCODING == "utf-8"
    assert DEFAULT_TIMEZONE == "America/Sao_Paulo"


def test_database_defaults():
    """Verifica as configurações padrão do banco."""

    assert DEFAULT_DATABASE_FILENAME == "ppp.db"


def test_logging_defaults():
    """Verifica as configurações padrão de log."""

    assert DEFAULT_LOG_LEVEL == "INFO"


def test_upload_defaults():
    """Verifica o tamanho máximo de upload."""

    assert MAX_UPLOAD_SIZE == 50 * MEGABYTE


def test_document_defaults():
    """Verifica os caminhos e arquivos padrão."""

    assert DEFAULT_OUTPUT_DIRECTORY == "output"
    assert DEFAULT_WORD_TEMPLATE == "PPP_Template.docx"


