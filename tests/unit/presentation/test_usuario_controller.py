"""Testes para UsuarioController."""

import pytest
from src.presentation.controllers.usuario_controller import UsuarioController
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.domain.entities.usuario import Usuario


def gerar_cpf_valido(numero_base: int) -> str:
    """Gera um CPF válido."""
    base_str = str(numero_base).zfill(9)
    soma = sum(int(base_str[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    base_com_d1 = base_str + str(digito1)
    soma = sum(int(base_com_d1[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    return base_str + str(digito1) + str(digito2)


@pytest.fixture
def repo():
    return UsuarioRepository()


@pytest.fixture
def controller(repo):
    return UsuarioController(repo)


# CRIAR USUARIO
def test_criar_usuario_sucesso(controller):
    """Testa criação de usuário via controller."""
    resposta = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta["sucesso"]
    assert resposta["usuario_id"] is not None


def test_criar_usuario_erro_email_invalido(controller):
    """Testa criação com email inválido."""
    resposta = controller.criar_usuario({
        "nome": "Werner",
        "email": "invalido",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert not resposta["sucesso"]


# LISTAR USUARIOS
def test_listar_usuarios_vazio(controller):
    """Testa listagem quando não há usuários."""
    resposta = controller.listar_usuarios()
    assert resposta["sucesso"]
    assert len(resposta["usuarios"]) == 0


def test_listar_usuarios_com_dados(controller):
    """Testa listagem com usuários."""
    # Criar
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })

    # Listar
    resposta = controller.listar_usuarios()
    assert resposta["sucesso"]
    assert len(resposta["usuarios"]) == 1
    assert resposta["usuarios"][0]["nome"] == "Werner"


# ATUALIZAR CARGO
def test_atualizar_cargo_sucesso(controller, repo):
    """Testa atualização de cargo."""
    # Criar
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    repo.salvar(usuario)

    # Atualizar
    resposta = controller.atualizar_cargo(1, {"novo_cargo": "Senior Dev"})
    assert resposta["sucesso"]

    # Verificar
    usuarios = controller.listar_usuarios()
    assert usuarios["usuarios"][0]["cargo"] == "Senior Dev"


# ATUALIZAR EMPRESA
def test_atualizar_empresa_sucesso(controller, repo):
    """Testa atualização de empresa."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="Empresa A",
        cargo="Dev"
    )
    repo.salvar(usuario)

    resposta = controller.atualizar_empresa(1, {"nova_empresa": "Empresa B"})
    assert resposta["sucesso"]

    usuarios = controller.listar_usuarios()
    assert usuarios["usuarios"][0]["empresa"] == "Empresa B"


# DESATIVAR USUARIO
def test_desativar_usuario_sucesso(controller, repo):
    """Testa desativação de usuário."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    repo.salvar(usuario)

    resposta = controller.desativar_usuario(1)
    assert resposta["sucesso"]

    usuarios = controller.listar_usuarios()
    assert len(usuarios["usuarios"]) == 0
