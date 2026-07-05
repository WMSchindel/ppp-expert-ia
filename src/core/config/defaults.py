"""
Módulo: defaults.py

Centraliza os valores padrão utilizados pela aplicação.

Este módulo contém apenas constantes. Nenhuma lógica de negócio
ou leitura de configuração deve ser implementada aqui.

Autor:
Werner Schindel

Projeto:
PPP Expert IA
"""

# =============================================================================
# Configurações Gerais
# =============================================================================

DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_ENCODING = "utf-8"
DEFAULT_TIMEZONE = "America/Sao_Paulo"

# =============================================================================
# Banco de Dados
# =============================================================================

DEFAULT_DATABASE_NAME = "ppp.db"

# =============================================================================
# Logging
# =============================================================================

DEFAULT_LANGUAGE: str = "pt-BR"
DEFAULT_ENCODING: str = "utf-8"
MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024

# =============================================================================
# Uploads
# =============================================================================

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
