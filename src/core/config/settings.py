"""
Configurações globais da aplicação.

Este módulo centraliza todas as configurações utilizadas pelo
PPP Expert IA.
"""

from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from core.config.defaults import (
    DEFAULT_DATABASE_FILENAME,
    DEFAULT_ENCODING,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LANGUAGE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_RETENTION,
    DEFAULT_LOG_ROTATION,
    DEFAULT_OUTPUT_DIRECTORY,
    DEFAULT_TIMEZONE,
    DEFAULT_WORD_TEMPLATE,
    MAX_UPLOAD_SIZE,
)

from core.config.environments import Environment


class Settings(BaseSettings):
    """Configurações globais da aplicação."""

    # =========================================================================
    # Ambiente
    # =========================================================================

    environment: Environment = DEFAULT_ENVIRONMENT

    # =========================================================================
    # Configuração Geral
    # =========================================================================

    language: str = DEFAULT_LANGUAGE
    encoding: str = DEFAULT_ENCODING
    timezone: str = DEFAULT_TIMEZONE


    # =========================================================================
    # Banco de Dados
    # =========================================================================

    database_filename: str = DEFAULT_DATABASE_FILENAME

    # =========================================================================
    # Logging
    # =========================================================================

    log_level: str = DEFAULT_LOG_LEVEL
    log_rotation: str = DEFAULT_LOG_ROTATION
    log_retention: str = DEFAULT_LOG_RETENTION

    # =========================================================================
    # Upload
    # =========================================================================

    max_upload_size: int = MAX_UPLOAD_SIZE

    # =========================================================================
    # Documentos
    # =========================================================================

    output_directory: str = DEFAULT_OUTPUT_DIRECTORY
    word_template: str = DEFAULT_WORD_TEMPLATE

    # =========================================================================
    # Configuração do Pydantic
    # =========================================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================================
    # Propriedades
    # =========================================================================

    @property
    def project_root(self) -> Path:
        """Retorna o diretório raiz do projeto."""
        return Path(__file__).resolve().parents[3]

    @property
    def database_directory(self) -> Path:
        """Retorna o diretório do banco de dados."""
        return self.project_root / "database"

    @property
    def output_directory_path(self) -> Path:
        """Retorna o diretório de saída."""
        return self.project_root / self.output_directory


# =============================================================================
# Instância global de configurações
# =============================================================================

settings = Settings()
