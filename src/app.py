from config.settings import settings
from utils.logger import logger


class App:

    def __init__(self):
        logger.info("Inicializando aplicação...")

    def run(self):
        print("=" * 60)
        print(settings.APP_NAME)
        print(f"Versão {settings.APP_VERSION}")
        print("=" * 60)

        logger.success("Sistema iniciado com sucesso.")
        