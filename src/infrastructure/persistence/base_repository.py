"""
Classe base para repositórios com suporte a logging.

Repositórios devem herdar desta classe para obter automaticamente
logging de operações de persistência.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from src.core.logging import logger


T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Classe base para todos os repositórios de persistência.

    Fornece logging automático para operações comuns:
    - Salvar entidades
    - Buscar entidades
    - Deletar entidades
    - Atualizar entidades
    """

    def __init__(self, session=None):
        """Inicializa o repositório com logging."""
        nome_repo = self.__class__.__name__
        logger.info(f"Repositório {nome_repo} inicializado")
        self.session = session

    @abstractmethod
    def salvar(self, entidade: T) -> T:
        """Salva uma entidade."""
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> T:
        """Busca uma entidade por ID."""
        pass

    @abstractmethod
    def listar_todos(self) -> List[T]:
        """Lista todas as entidades."""
        pass

    @abstractmethod
    def deletar(self, entidade: T) -> None:
        """Deleta uma entidade."""
        pass

    def _log_operacao(self, operacao: str, entidade_nome: str):
        """Registra uma operação no log."""
        logger.info(f"{operacao}: {entidade_nome}")

    def _log_erro(self, operacao: str, entidade_nome: str, erro: Exception):
        """Registra um erro no log."""
        logger.error(f"Erro ao {operacao.lower()} {entidade_nome}: {erro}")
