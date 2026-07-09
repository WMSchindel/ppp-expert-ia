"""Testes para Usuario entity."""

import pytest
from datetime import datetime
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF


@pytest.fixture
def cpf_valido():
    return CPF("11144477735")


def test_usuario_pode_ser_criado(cpf_valido):
    usuario = Usuario(
        nome="Werner Schindel",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="PPP Expert IA",
        cargo="Desenvolvedor"
    )
    assert usuario is not None


def test_usuario_tem_nome(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    assert usuario.nome == "Werner"


def test_usuario_tem_email(cpf_valido):
    email = Email("werner@example.com")
    usuario = Usuario(
        nome="Werner",
        email=email,
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    assert usuario.email == email


def test_usuario_tem_cpf(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    assert usuario.cpf == cpf_valido


def test_usuario_ativo_por_default(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    assert usuario.ativo is True


def test_usuario_tem_data_criacao(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    assert isinstance(usuario.data_criacao, datetime)


def test_usuario_desativar(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    usuario.desativar()
    assert usuario.ativo is False


def test_usuario_atualizar_cargo(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa",
        cargo="Dev"
    )
    usuario.atualizar_cargo("Senior Developer")
    assert usuario.cargo == "Senior Developer"


def test_usuario_atualizar_empresa(cpf_valido):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=cpf_valido,
        empresa="Empresa A",
        cargo="Dev"
    )
    usuario.atualizar_empresa("Empresa B")
    assert usuario.empresa == "Empresa B"


def test_usuario_nome_vazio_falha(cpf_valido):
    with pytest.raises(ValueError):
        Usuario(
            nome="",
            email=Email("werner@example.com"),
            cpf=cpf_valido,
            empresa="Empresa",
            cargo="Dev"
        )
