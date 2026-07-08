"""
Módulo: logger.py

Implementação centralizada de logging utilizando Loguru.

Este módulo encapsula toda a complexidade da configuração do Loguru,
fornecendo uma interface simples e consistente para toda a aplicação.

Autor:
Werner Schindel

Projeto:
PPP Expert IA
"""

import sys
from pathlib import Path

from loguru import logger as _loguru_logger

from core.config.settings import settings


def _configure_logger() -> None:
    """
    Configura o logger global com base nas configurações da aplicação.

    Remove os handlers padrão e configura:
    - Console: exibição colorida das mensagens
    - Arquivo: armazenamento completo dos logs
    """

    # Remove o handler padrão do loguru
    _loguru_logger.remove()

    # Cria o diretório de logs se não existir
    settings.logs_path.mkdir(parents=True, exist_ok=True)

    # Configura saída para console
    _loguru_logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        level=settings.log_level,
        colorize=True,
    )

    # Configura saída para arquivo com rotação
    log_file = settings.logs_path / "ppp_expert_ia.log"

    _loguru_logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        level=settings.log_level,
        rotation=settings.log_rotation,
        retention=settings.log_retention,
        encoding="utf-8",
    )


# Configura o logger na importação
_configure_logger()

# Exporta o logger configurado
logger = _loguru_logger
