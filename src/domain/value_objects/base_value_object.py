"""
Classe base para Value Objects do domínio com suporte a logging.

Objetos de valor devem herdar desta classe para obter automaticamente
logging de criação e validação.
"""

from abc import ABC
from src.core.logging import logger


class ValueObject(ABC):
    """Classe base para todos os objetos de valor do domínio.

    Objetos de valor são objetos imutáveis que representam um valor.
    Fornece logging automático do ciclo de vida:
    - Eventos de criação
    - Operações de validação
    """

    def __init__(self, valor):
        """Inicializa o objeto de valor com logging automático."""
        nome_vo = self.__class__.__name__
        logger.debug(f"ValueObject {nome_vo} criado")
        logger.debug(f"Tipo de valor: {type(valor).__name__}")
        self._valor = valor

    @property
    def valor(self):
        """Obtém o valor encapsulado."""
        return self._valor

    def __repr__(self) -> str:
        """Representação em string para logging."""
        return f"{self.__class__.__name__}({self._valor})"

    def __eq__(self, outro) -> bool:
        """Verifica igualdade com outro objeto de valor."""
        if not isinstance(outro, self.__class__):
            logger.debug(f"Comparação ValueObject: {self.__class__.__name__} != {type(outro).__name__}")
            return False
        return self._valor == outro._valor

    def __hash__(self) -> int:
        """Torna o objeto de valor hashable."""
        return hash(self._valor)
