"""
===============================================================================
Projeto    : PPP Expert IA
Plataforma : SST Platform
Framework  : SST Core

Arquivo    : paths.py

Descrição:
    Gerenciamento centralizado dos caminhos da aplicação.
===============================================================================
"""

from pathlib import Path


class Paths:
    """Centraliza todos os caminhos utilizados pela aplicação."""

    def __init__(self) -> None:

        # Diretório raiz do projeto
        self.project_root = Path(__file__).resolve().parents[2]

        # Código-fonte
        self.src = self.project_root / "src"

        # Recursos
        self.assets = self.project_root / "assets"
        self.docs = self.project_root / "docs"
        self.templates = self.project_root / "templates"

        # Dados da aplicação
        self.data = self.project_root / "data"

        self.database = self.data / "database"
        self.logs = self.data / "logs"
        self.uploads = self.data / "uploads"
        self.output = self.data / "output"
        self.backups = self.data / "backups"

        # Testes
        self.tests = self.project_root / "tests"

    def initialize(self) -> None:
        """Cria automaticamente a estrutura necessária."""

        directories = (
            self.assets,
            self.docs,
            self.templates,
            self.data,
            self.database,
            self.logs,
            self.uploads,
            self.output,
            self.backups,
            self.tests,
        )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


paths = Paths()
