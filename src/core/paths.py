from pathlib import Path


class Paths:
    """Centraliza todos os caminhos do projeto."""

    def __init__(self):

        self.PROJECT_ROOT = Path(__file__).resolve().parents[2]

        self.SRC = self.PROJECT_ROOT / "src"

        self.DATA = self.PROJECT_ROOT / "data"

        self.DATABASE = self.DATA / "database"

        self.BACKUPS = self.DATA / "backups"

        self.UPLOADS = self.DATA / "uploads"

        self.OUTPUT = self.DATA / "output"

        self.LOGS = self.DATA / "logs"

        self.DOCS = self.PROJECT_ROOT / "docs"

        self.TEMPLATES = self.PROJECT_ROOT / "templates"

        self.ASSETS = self.PROJECT_ROOT / "assets"

    def create_directories(self):

        directories = [

            self.DATA,

            self.DATABASE,

            self.BACKUPS,

            self.UPLOADS,

            self.OUTPUT,

            self.LOGS

        ]

        for directory in directories:

            directory.mkdir(parents=True, exist_ok=True)


paths = Paths()