from core.config.settings import Settings

def test_settings_can_be_instantiated():
    """Verifica se a classe Settings pode ser instanciada."""

    settings = Settings()

    assert settings is not None


from core.config.defaults import (
    DEFAULT_ENCODING,
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)


def test_default_general_settings():
    """Verifica as configurações gerais padrão."""

    settings = Settings()

    assert settings.language == DEFAULT_LANGUAGE
    assert settings.encoding == DEFAULT_ENCODING
    assert settings.timezone == DEFAULT_TIMEZONE

from pathlib import Path

from core.config.defaults import (
    DEFAULT_DATABASE_FILENAME,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_RETENTION,
    DEFAULT_LOG_ROTATION,
    DEFAULT_OUTPUT_DIRECTORY,
    DEFAULT_WORD_TEMPLATE,
    MAX_UPLOAD_SIZE,
)

def test_database_settings():
    """Verifica as configurações do banco de dados."""

    settings = Settings()

    assert settings.database_filename == DEFAULT_DATABASE_FILENAME


def test_logging_settings():
    """Verifica apenas os tipos das configurações de logging."""

    settings = Settings()

    assert isinstance(settings.log_level, str)
    assert isinstance(settings.log_rotation, str)
    assert isinstance(settings.log_retention, str)


def test_upload_settings():
    """Verifica as configurações de upload."""

    settings = Settings()

    assert settings.max_upload_size == MAX_UPLOAD_SIZE


def test_document_settings():
    """Verifica as configurações de documentos."""

    settings = Settings()

    assert settings.output_directory == DEFAULT_OUTPUT_DIRECTORY
    assert settings.word_template == DEFAULT_WORD_TEMPLATE


def test_project_root():
    """Verifica se o diretório raiz existe."""

    settings = Settings()

    assert isinstance(settings.project_root, Path)
    assert settings.project_root.exists()

def test_database_directory():
    """Verifica o caminho do diretório de banco de dados."""

    settings = Settings()

    assert settings.database_directory.name == "database"


def test_output_directory_path():
    """Verifica o caminho do diretório de saída."""

    settings = Settings()

    assert settings.output_directory_path.name == settings.output_directory