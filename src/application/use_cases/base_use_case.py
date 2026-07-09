"""
Classe base para Casos de Uso da aplicação com suporte a logging.

Casos de uso devem herdar desta classe para obter automaticamente
logging de execução e operações.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.core.logging import logger


@dataclass
class UseCaseRequest:
    """Classe base para requisições de casos de uso."""
    pass


@dataclass
class UseCaseResponse:
    """Classe base para respostas de casos de uso."""
    sucesso: bool
    mensagem: str = ""


class UseCase(ABC):
    """Classe base para todos os casos de uso da aplicação.

    Fornece logging automático do ciclo de vida do caso de uso:
    - Início de execução
    - Requisição recebida
    - Conclusão
    - Erros
    """

    @abstractmethod
    def executar(self, requisicao: UseCaseRequest) -> UseCaseResponse:
        """Executa o caso de uso.

        Este método deve ser implementado pelas subclasses.
        O logging é feito automaticamente antes e depois.

        Args:
            requisicao: Dados de entrada do caso de uso

        Returns:
            Resposta do caso de uso
        """
        pass

    def __call__(self, requisicao: UseCaseRequest) -> UseCaseResponse:
        """Permite que o caso de uso seja chamado como função."""
        nome_caso_uso = self.__class__.__name__
        logger.info(f"Caso de Uso {nome_caso_uso} iniciado")
        logger.debug(f"Requisição: {requisicao.__class__.__name__}")

        try:
            resposta = self.executar(requisicao)
            logger.info(f"Caso de Uso {nome_caso_uso} concluído: {resposta.sucesso}")
            if resposta.mensagem:
                logger.debug(f"Mensagem: {resposta.mensagem}")
            return resposta
        except Exception as e:
            logger.error(f"Caso de Uso {nome_caso_uso} falhou: {e}")
            raise
