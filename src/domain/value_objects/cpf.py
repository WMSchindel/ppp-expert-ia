"""
Value Object para representar um CPF.

CPF é um valor imutável que representa um número de CPF válido.
Valida formato e dígitos verificadores.
"""

from src.domain.value_objects.base_value_object import ValueObject
from src.core.logging import logger


class CPF(ValueObject):
    """Representa um CPF válido.

    CPF é um value object que:
    - Valida formato (11 dígitos)
    - Valida dígitos verificadores (mod 11)
    - Normaliza removendo caracteres especiais
    - Fornece igualdade por valor
    """

    def __init__(self, numero: str):
        """Inicializa um CPF com validação.

        Args:
            numero: String com CPF (com ou sem formatação)

        Raises:
            ValueError: Se CPF inválido
        """
        # Normalizar: remover formatação
        numero_limpo = numero.replace(".", "").replace("-", "").strip()

        # Validar tamanho
        if len(numero_limpo) != 11:
            logger.warning(f"CPF tamanho inválido: {len(numero_limpo)}")
            raise ValueError("CPF deve ter 11 dígitos")

        # Validar se são dígitos
        if not numero_limpo.isdigit():
            logger.warning(f"CPF com caracteres não numéricos: {numero_limpo}")
            raise ValueError("CPF deve conter apenas dígitos")

        # Validar CPF com todos os dígitos iguais
        if len(set(numero_limpo)) == 1:
            logger.warning(f"CPF com todos dígitos iguais: {numero_limpo}")
            raise ValueError("CPF com todos dígitos iguais é inválido")

        # Validar dígitos verificadores
        if not self._validar_cpf(numero_limpo):
            logger.warning(f"CPF com dígitos verificadores inválidos: {numero_limpo}")
            raise ValueError("CPF com dígitos verificadores inválidos")

        # Armazenar com formatação padrão
        cpf_formatado = f"{numero_limpo[0:3]}.{numero_limpo[3:6]}.{numero_limpo[6:9]}-{numero_limpo[9:11]}"
        super().__init__(cpf_formatado)

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida dígitos verificadores do CPF.

        Args:
            cpf: String com 11 dígitos

        Returns:
            True se válido, False caso contrário
        """
        # Primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        if int(cpf[9]) != digito1:
            return False

        # Segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return int(cpf[10]) == digito2

    def __repr__(self) -> str:
        """Representação do CPF."""
        return f"CPF({self._valor})"
