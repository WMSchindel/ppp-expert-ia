"""
defaults.py

Define os valores padrão utilizados pela aplicação.

Autor:
Werner Schindel

Projeto:
PPP Expert IA
"""

# Configurações gerais
DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_ENCODING = "utf-8"
DEFAULT_TIMEZONE = "America/Sao_Paulo"

# Diretórios
DEFAULT_DATABASE_NAME = "ppp.db"

# Logging
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_ROTATION = "10 MB"
DEFAULT_LOG_RETENTION = "30 days"

# Uploads
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
