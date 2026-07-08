"""
Módulo: defaults.py

Centraliza todos os valores padrão utilizados pela aplicação.
"""

from typing import Final

from core.config.environments import Environment


# =============================================================================
# Unidades de Medida
# =============================================================================

KILOBYTE: Final[int] = 1024
MEGABYTE: Final[int] = 1024 * KILOBYTE
GIGABYTE: Final[int] = 1024 * MEGABYTE


# =============================================================================
# Ambiente
# =============================================================================

DEFAULT_ENVIRONMENT: Final[Environment] = Environment.DEVELOPMENT


# =============================================================================
# Configuração Geral
# =============================================================================

DEFAULT_ENCODING: Final[str] = "utf-8"
DEFAULT_LANGUAGE: Final[str] = "pt-BR"
DEFAULT_TIMEZONE: Final[str] = "America/Sao_Paulo"


# =============================================================================
# Banco de Dados
# =============================================================================

DEFAULT_DATABASE_FILENAME: Final[str] = "ppp.db"


# =============================================================================
# Logging
# =============================================================================

DEFAULT_LOG_LEVEL: Final[str] = "INFO"
DEFAULT_LOG_ROTATION: Final[str] = "10 MB"
DEFAULT_LOG_RETENTION: Final[str] = "30 days"


# =============================================================================
# Upload
# =============================================================================

MAX_UPLOAD_SIZE: Final[int] = 50 * MEGABYTE


# =============================================================================
# Documentos
# =============================================================================

DEFAULT_OUTPUT_DIRECTORY: Final[str] = "output"
DEFAULT_WORD_TEMPLATE: Final[str] = "PPP_Template.docx"