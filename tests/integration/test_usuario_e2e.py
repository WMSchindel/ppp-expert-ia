"""Testes E2E para fluxos completos de Usuario."""

import pytest
from src.presentation.controllers.usuario_controller import UsuarioController
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository


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
def controller():
    repo = UsuarioRepository()
    return UsuarioController(repo)


# E2E-001: Criar e Listar Usuario
def test_e2e_criar_e_listar(controller):
    """Fluxo: Criar usuario → Listar → Verificar."""
    # Criar
    resposta_criar = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta_criar["sucesso"]
    usuario_id = resposta_criar["usuario_id"]

    # Listar
    resposta_listar = controller.listar_usuarios()
    assert resposta_listar["sucesso"]
    assert len(resposta_listar["usuarios"]) == 1
    assert resposta_listar["usuarios"][0]["id"] == usuario_id
    assert resposta_listar["usuarios"][0]["nome"] == "Werner"


# E2E-002: Criar, Atualizar Cargo, Verificar
def test_e2e_criar_atualizar_cargo(controller):
    """Fluxo: Criar → Atualizar cargo → Listar → Verificar."""
    # Criar
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })

    # Atualizar
    resposta_atualizar = controller.atualizar_cargo(1, {"novo_cargo": "Senior Dev"})
    assert resposta_atualizar["sucesso"]

    # Verificar
    resposta_listar = controller.listar_usuarios()
    assert resposta_listar["usuarios"][0]["cargo"] == "Senior Dev"


# E2E-003: Criar, Atualizar Empresa, Verificar
def test_e2e_criar_atualizar_empresa(controller):
    """Fluxo: Criar → Atualizar empresa → Listar → Verificar."""
    # Criar
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "Empresa A",
        "cargo": "Dev"
    })

    # Atualizar
    resposta_atualizar = controller.atualizar_empresa(1, {"nova_empresa": "Empresa B"})
    assert resposta_atualizar["sucesso"]

    # Verificar
    resposta_listar = controller.listar_usuarios()
    assert resposta_listar["usuarios"][0]["empresa"] == "Empresa B"


# E2E-004: Criar e Desativar Usuario
def test_e2e_criar_e_desativar(controller):
    """Fluxo: Criar → Desativar → Listar → Verificar ausência."""
    # Criar
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })

    # Verificar que está na lista
    resposta_antes = controller.listar_usuarios()
    assert len(resposta_antes["usuarios"]) == 1

    # Desativar
    resposta_desativar = controller.desativar_usuario(1)
    assert resposta_desativar["sucesso"]

    # Verificar que não está mais na lista
    resposta_depois = controller.listar_usuarios()
    assert len(resposta_depois["usuarios"]) == 0


# E2E-005: Múltiplos Usuarios - Validar Isolamento
def test_e2e_multiplos_usuarios(controller):
    """Fluxo: Criar A → Criar B → Listar (2) → Desativar A → Listar (1)."""
    # Criar A
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })

    # Criar B
    controller.criar_usuario({
        "nome": "João",
        "email": "joao@example.com",
        "cpf": gerar_cpf_valido(214741688),
        "empresa": "PPP",
        "cargo": "Analista"
    })

    # Listar - deve ter 2
    resposta_dois = controller.listar_usuarios()
    assert len(resposta_dois["usuarios"]) == 2

    # Desativar A
    controller.desativar_usuario(1)

    # Listar - deve ter 1
    resposta_um = controller.listar_usuarios()
    assert len(resposta_um["usuarios"]) == 1
    assert resposta_um["usuarios"][0]["nome"] == "João"


# E2E-006: Validação de Duplicatas - Email
def test_e2e_email_duplicado(controller):
    """Fluxo: Criar com email X → Tentar criar com email X → Erro."""
    # Criar primeiro usuario
    resposta1 = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta1["sucesso"]

    # Tentar criar com email duplicado
    resposta2 = controller.criar_usuario({
        "nome": "Outro",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(214741688),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert not resposta2["sucesso"]
    assert "Email" in resposta2["mensagem"]


# E2E-007: Validação de Duplicatas - CPF
def test_e2e_cpf_duplicado(controller):
    """Fluxo: Criar com CPF X → Tentar criar com CPF X → Erro."""
    cpf = gerar_cpf_valido(111444777)

    # Criar primeiro usuario
    resposta1 = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": cpf,
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta1["sucesso"]

    # Tentar criar com CPF duplicado
    resposta2 = controller.criar_usuario({
        "nome": "Outro",
        "email": "outro@example.com",
        "cpf": cpf,
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert not resposta2["sucesso"]
    assert "CPF" in resposta2["mensagem"]
