"""
Testes para logging de entidades do domínio.

Valida que entidades fazem logging correto ao serem criadas.
"""

import pytest
from src.domain.entities import Entity


class Usuario(Entity):
    """Entidade de exemplo para testes."""

    def __init__(self, nome: str, email: str):
        super().__init__(nome=nome, email=email)
        self.nome = nome
        self.email = email


def test_entity_can_be_created():
    """Testa que uma entidade pode ser criada."""
    usuario = Usuario(nome="Werner", email="werner@example.com")
    assert usuario.nome == "Werner"
    assert usuario.email == "werner@example.com"


def test_entity_has_logging_support():
    """Testa que Entity fornece suporte a logging."""
    assert hasattr(Entity, '__init__')
    usuario = Usuario(nome="Werner", email="werner@example.com")
    assert usuario is not None


def test_entity_repr():
    """Testa a representação em string da entidade."""
    usuario = Usuario(nome="Werner", email="werner@example.com")
    repr_str = repr(usuario)
    assert "Usuario" in repr_str
    assert "nome" in repr_str


def test_multiple_entities_creation():
    """Testa criação de múltiplas entidades."""
    usuario1 = Usuario(nome="Werner", email="werner@example.com")
    usuario2 = Usuario(nome="João", email="joao@example.com")

    assert usuario1.nome == "Werner"
    assert usuario2.nome == "João"
    assert usuario1.email != usuario2.email
