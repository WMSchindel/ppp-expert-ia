from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações globais da aplicação."""

    app_name: str = "PPP Expert IA"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str

    openai_api_key: str = ""

    log_level: str = "INFO"

    upload_dir: str = "uploads"
    output_dir: str = "output"
    log_dir: str = "logs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    @property
    def database_path(self) -> Path:
        return self.project_root / "database"

    @property
    def uploads_path(self) -> Path:
        return self.project_root / self.upload_dir

    @property
    def output_path(self) -> Path:
        return self.project_root / self.output_dir

    @property
    def logs_path(self) -> Path:
        return self.project_root / self.log_dir


settings = Settings()