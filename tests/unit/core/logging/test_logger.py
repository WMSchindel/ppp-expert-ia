"""
Testes unitários do módulo logger.py.

Verifica se o logger está configurado corretamente e funciona
conforme esperado.
"""

import tempfile
from pathlib import Path

from core.logging.logger import logger


def test_logger_can_be_imported():
    """Verifica se o logger pode ser importado sem erros."""

    assert logger is not None


def test_logger_has_required_methods():
    """Verifica se o logger possui os métodos esperados."""

    required_methods = ["debug", "info", "success", "warning", "error", "critical"]

    for method in required_methods:
        assert hasattr(logger, method), f"Logger não possui o método {method}"


def test_logger_can_log_messages():
    """Verifica se o logger consegue registrar mensagens em todos os níveis."""

    try:
        logger.debug("Mensagem de debug")
        logger.info("Mensagem de informação")
        logger.success("Mensagem de sucesso")
        logger.warning("Mensagem de aviso")
        logger.error("Mensagem de erro")
        logger.critical("Mensagem crítica")
    except Exception as e:
        assert False, f"Erro ao registrar mensagens: {e}"


def test_logger_is_singleton():
    """Verifica se o logger é uma única instância (singleton)."""

    from core.logging.logger import logger as logger2

    assert logger is logger2, "Logger não é um singleton"


def test_logger_configuration():
    """Verifica se o logger foi configurado com os handlers corretos."""

    # O logger deve ter handlers configurados
    assert len(logger._core.handlers) > 0, "Logger não possui handlers configurados"
