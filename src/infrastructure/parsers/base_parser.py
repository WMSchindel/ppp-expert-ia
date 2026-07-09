"""
Classe base para parsers com suporte a logging.

Parsers devem herdar desta classe para obter automaticamente
logging de operações de parsing de dados.
"""

from abc import ABC, abstractmethod
from typing import Any, List
from pathlib import Path
from src.core.logging import logger


class Parser(ABC):
    """Classe base para todos os parsers de dados.

    Fornece logging automático para operações:
    - Início do parsing
    - Conclusão do parsing
    - Erros durante parsing
    - Quantidade de registros processados
    """

    def __init__(self, tipo_entrada: str = None):
        """Inicializa o parser com logging."""
        nome_parser = self.__class__.__name__
        logger.info(f"Parser {nome_parser} inicializado")
        self.tipo_entrada = tipo_entrada or "desconhecido"

    @abstractmethod
    def parse(self, entrada: Any) -> List[dict]:
        """Faz parsing de dados de entrada.

        Args:
            entrada: Dados para fazer parsing (arquivo, string, etc)

        Returns:
            Lista de dicionários com dados parseados
        """
        pass

    def _log_inicio_parsing(self, arquivo: str = None):
        """Registra início do parsing."""
        logger.info(f"Iniciando parsing de {self.tipo_entrada}")
        if arquivo:
            logger.debug(f"Arquivo: {arquivo}")

    def _log_conclusao_parsing(self, quantidade_registros: int):
        """Registra conclusão do parsing."""
        logger.info(f"Parsing concluído com sucesso")
        logger.debug(f"Registros processados: {quantidade_registros}")

    def _log_erro_parsing(self, erro: Exception, linha: int = None):
        """Registra erro durante parsing."""
        if linha:
            logger.error(f"Erro ao fazer parsing na linha {linha}: {erro}")
        else:
            logger.error(f"Erro ao fazer parsing: {erro}")

    def _log_validacao(self, registros_validos: int, registros_invalidos: int):
        """Registra resultado da validação."""
        logger.debug(f"Registros válidos: {registros_validos}")
        if registros_invalidos > 0:
            logger.warning(f"Registros inválidos: {registros_invalidos}")
