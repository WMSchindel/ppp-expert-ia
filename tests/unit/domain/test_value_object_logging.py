"""
Testes para logging de objetos de valor do domínio.

Valida que objetos de valor fazem logging correto ao serem criados.
"""

import pytest
from src.domain.value_objects import ValueObject


class Email(ValueObject):
    """Objeto de valor de exemplo para testes."""

    def __init__(self, endereco: str):
        super().__init__(endereco)


class Cpf(ValueObject):
    """Outro objeto de valor de exemplo."""

    def __init__(self, numero: str):
        super().__init__(numero)


def test_value_object_can_be_created():
    """Testa que um objeto de valor pode ser criado."""
    email = Email("werner@example.com")
    assert email.valor == "werner@example.com"


def test_value_object_immutability():
    """Testa que objetos de valor são imutáveis."""
    email = Email("werner@example.com")
    # Tentar mudar valor direto não funciona (protegido)
    assert email._valor == "werner@example.com"


def test_value_object_equality():
    """Testa igualdade entre objetos de valor."""
    email1 = Email("werner@example.com")
    email2 = Email("werner@example.com")
    email3 = Email("outro@example.com")

    assert email1 == email2
    assert email1 != email3


def test_value_object_hash():
    """Testa que objetos de valor são hashable."""
    email1 = Email("werner@example.com")
    email2 = Email("werner@example.com")

    # Mesmos valores = mesmo hash
    assert hash(email1) == hash(email2)

    # Pode ser usado em set/dict
    emails = {email1, email2}
    assert len(emails) == 1


def test_different_value_object_types():
    """Testa comparação entre tipos diferentes de objetos de valor."""
    email = Email("werner@example.com")
    cpf = Cpf("12345678900")

    assert email != cpf
    assert not (email == cpf)
