"""Testes para CPF value object."""

import pytest
from src.domain.value_objects.cpf import CPF


def test_cpf_valido():
    """Teste com CPF válido."""
    cpf = CPF("11144477735")
    assert "111" in cpf.valor


def test_cpf_com_formatacao():
    """CPF com formatação deve ser aceito."""
    cpf = CPF("111.444.777-35")
    assert "111" in cpf.valor


def test_cpf_invalido_tamanho():
    """CPF com tamanho incorreto deve falhar."""
    with pytest.raises(ValueError):
        CPF("123")


def test_cpf_invalido_caracteres():
    """CPF com caracteres não-numéricos deve falhar."""
    with pytest.raises(ValueError):
        CPF("1ab45678901")


def test_cpf_todos_digitos_iguais():
    """CPF com todos dígitos iguais deve falhar."""
    with pytest.raises(ValueError):
        CPF("11111111111")


def test_cpf_igualdade():
    """CPFs com mesmo valor devem ser iguais."""
    cpf1 = CPF("11144477735")
    cpf2 = CPF("111.444.777-35")
    assert cpf1 == cpf2


def test_cpf_hash():
    """CPFs iguais devem ter mesmo hash."""
    cpf1 = CPF("11144477735")
    cpf2 = CPF("111.444.777-35")
    assert hash(cpf1) == hash(cpf2)
