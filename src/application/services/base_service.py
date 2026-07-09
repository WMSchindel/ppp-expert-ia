"""
Classe base para Services da aplicação com suporte a logging.

Serviços devem herdar desta classe para obter automaticamente
logging de execução e operações.
"""

from abc import ABC, abstractmethod
from src.core.logging import logger


class Service(ABC):
    """Classe base para todos os serviços de aplicação.

    Fornece logging automático do ciclo de vida do serviço:
    - Início de execução
    - Parâmetros recebidos
    - Conclusão
    - Erros
    """

    @abstractmethod
    def executar(self, *args, **kwargs):
        """Executa o serviço.

        Este método deve ser implementado pelas subclasses.
        O logging é feito automaticamente antes e depois.
        """
        pass

    def __call__(self, *args, **kwargs):
        """Permite que o serviço seja chamado como função."""
        nome_servico = self.__class__.__name__
        logger.info(f"Serviço {nome_servico} iniciado")

        parametros = {}
        if args:
            parametros['args'] = [str(arg)[:50] for arg in args]
        if kwargs:
            parametros['kwargs'] = {k: str(v)[:50] for k, v in kwargs.items()}

        if parametros:
            logger.debug(f"Parâmetros: {parametros}")

        try:
            resultado = self.executar(*args, **kwargs)
            logger.info(f"Serviço {nome_servico} concluído com sucesso")
            return resultado
        except Exception as e:
            logger.error(f"Serviço {nome_servico} falhou: {e}")
            raise
