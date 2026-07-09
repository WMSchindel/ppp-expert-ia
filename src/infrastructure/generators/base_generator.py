"""
Classe base para geradores com suporte a logging.

Geradores devem herdar desta classe para obter automaticamente
logging de operações de geração de documentos.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from src.core.logging import logger


class Generator(ABC):
    """Classe base para todos os geradores de documentos.

    Fornece logging automático para operações:
    - Início da geração
    - Conclusão da geração
    - Erros durante geração
    """

    def __init__(self, output_dir: Path = None):
        """Inicializa o gerador com logging."""
        nome_gerador = self.__class__.__name__
        logger.info(f"Gerador {nome_gerador} inicializado")
        self.output_dir = output_dir

    @abstractmethod
    def gerar(self, dados: dict) -> Path:
        """Gera um documento a partir dos dados.

        Args:
            dados: Dicionário com dados para geração

        Returns:
            Caminho do arquivo gerado
        """
        pass

    def _log_inicio_geracao(self, tipo_documento: str):
        """Registra início da geração."""
        logger.info(f"Iniciando geração de {tipo_documento}")
        logger.debug(f"Diretório de saída: {self.output_dir}")

    def _log_conclusao_geracao(self, caminho_arquivo: Path):
        """Registra conclusão da geração."""
        tamanho_kb = caminho_arquivo.stat().st_size / 1024
        logger.info(f"Documento gerado com sucesso")
        logger.debug(f"Arquivo: {caminho_arquivo}")
        logger.debug(f"Tamanho: {tamanho_kb:.2f} KB")

    def _log_erro_geracao(self, tipo_documento: str, erro: Exception):
        """Registra erro durante geração."""
        logger.error(f"Erro ao gerar {tipo_documento}: {erro}")
