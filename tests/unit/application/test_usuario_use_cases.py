"""Testes para casos de uso de Usuário."""

import pytest
from src.application.use_cases.usuario_use_cases import (
    CriarUsuarioUseCase, CriarUsuarioRequest,
    AtualizarCargoUseCase, AtualizarCargoRequest,
    AtualizarEmpresaUseCase, AtualizarEmpresaRequest,
    DesativarUsuarioUseCase, DesativarUsuarioRequest,
    ListarUsuariosAtivosUseCase, ListarUsuariosAtivosRequest
)
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


# CRIAR USUARIO
def test_criar_usuario_sucesso(repo):
    caso = CriarUsuarioUseCase(repo)
    requisicao = CriarUsuarioRequest(
        nome="Werner",
        email="werner@example.com",
        cpf=gerar_cpf_valido(111444777),
        empresa="PPP",
        cargo="Dev"
    )
    resposta = caso(requisicao)
    assert resposta.sucesso
    assert resposta.usuario_id is not None


def test_criar_usuario_email_invalido(repo):
    caso = CriarUsuarioUseCase(repo)
    requisicao = CriarUsuarioRequest(
        nome="Werner",
        email="emailinvalido",
        cpf=gerar_cpf_valido(111444777),
        empresa="PPP",
        cargo="Dev"
    )
    resposta = caso(requisicao)
    assert not resposta.sucesso


def test_criar_usuario_cpf_invalido(repo):
    caso = CriarUsuarioUseCase(repo)
    requisicao = CriarUsuarioRequest(
        nome="Werner",
        email="werner@example.com",
        cpf="00000000000",
        empresa="PPP",
        cargo="Dev"
    )
    resposta = caso(requisicao)
    assert not resposta.sucesso


# ATUALIZAR CARGO
def test_atualizar_cargo_sucesso(repo):
    # Criar primeiro
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    repo.salvar(usuario)

    # Atualizar
    caso = AtualizarCargoUseCase(repo)
    requisicao = AtualizarCargoRequest(
        usuario_id=1,
        novo_cargo="Senior Dev"
    )
    resposta = caso(requisicao)
    assert resposta.sucesso

    # Verificar
    usuario_atualizado = repo.buscar_por_id(1)
    assert usuario_atualizado.cargo == "Senior Dev"


def test_atualizar_cargo_usuario_inexistente(repo):
    caso = AtualizarCargoUseCase(repo)
    requisicao = AtualizarCargoRequest(
        usuario_id=999,
        novo_cargo="Senior"
    )
    resposta = caso(requisicao)
    assert not resposta.sucesso


# ATUALIZAR EMPRESA
def test_atualizar_empresa_sucesso(repo):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="Empresa A",
        cargo="Dev"
    )
    repo.salvar(usuario)

    caso = AtualizarEmpresaUseCase(repo)
    requisicao = AtualizarEmpresaRequest(
        usuario_id=1,
        nova_empresa="Empresa B"
    )
    resposta = caso(requisicao)
    assert resposta.sucesso

    usuario_atualizado = repo.buscar_por_id(1)
    assert usuario_atualizado.empresa == "Empresa B"


# DESATIVAR USUARIO
def test_desativar_usuario_sucesso(repo):
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    repo.salvar(usuario)

    caso = DesativarUsuarioUseCase(repo)
    requisicao = DesativarUsuarioRequest(usuario_id=1)
    resposta = caso(requisicao)
    assert resposta.sucesso

    usuario_desativado = repo.buscar_por_id(1)
    assert not usuario_desativado.ativo


# LISTAR USUARIOS ATIVOS
def test_listar_usuarios_ativos(repo):
    # Criar 2 usuários
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Analista"
    )
    repo.salvar(usuario1)
    repo.salvar(usuario2)

    # Desativar um
    usuario1.desativar()

    # Listar
    caso = ListarUsuariosAtivosUseCase(repo)
    requisicao = ListarUsuariosAtivosRequest()
    resposta = caso(requisicao)

    assert resposta.sucesso
    assert len(resposta.usuarios) == 1
    assert resposta.usuarios[0]["nome"] == "João"


def test_listar_usuarios_vazios(repo):
    caso = ListarUsuariosAtivosUseCase(repo)
    requisicao = ListarUsuariosAtivosRequest()
    resposta = caso(requisicao)

    assert resposta.sucesso
    assert len(resposta.usuarios) == 0
