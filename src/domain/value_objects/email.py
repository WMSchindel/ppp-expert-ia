"""
Value Object para representar um email.

Email é um valor imutável que representa um endereço de correio eletrônico.
Valida formato básico e fornece igualdade por valor.
"""

from src.domain.value_objects.base_value_object import ValueObject
from src.core.logging import logger


class Email(ValueObject):
    """Representa um endereço de email válido.

    Email é um value object que:
    - Valida formato básico (@ e domínio)
    - Normaliza para lowercase
    - Fornece igualdade por valor
    """

    def __init__(self, endereco: str):
        """Inicializa um email com validação.

        Args:
            endereco: String com endereço de email

        Raises:
            ValueError: Se email inválido
        """
        endereco = endereco.strip().lower()

        if not endereco:
            logger.warning("Email vazio")
            raise ValueError("Email não pode ser vazio")

        if "@" not in endereco:
            logger.warning(f"Email sem @: {endereco}")
            raise ValueError("Email deve conter @")

        partes = endereco.split("@")
        if len(partes) != 2:
            logger.warning(f"Email com múltiplos @: {endereco}")
            raise ValueError("Email deve ter exatamente um @")

        usuario, dominio = partes

        if not usuario or not usuario.replace(".", "").replace("_", "").replace("-", "").isalnum():
            logger.warning(f"Parte do email inválida: {usuario}")
            raise ValueError("Parte antes do @ inválida")

        if not dominio or "." not in dominio:
            logger.warning(f"Domínio inválido: {dominio}")
            raise ValueError("Domínio deve ter ponto")

        super().__init__(endereco)

    def __repr__(self) -> str:
        """Representação do email."""
        return f"Email({self._valor})"
