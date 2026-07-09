"""Testes para UsuarioRepository."""

import pytest
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository


def gerar_cpf_valido(numero_base: int) -> str:
    """Gera um CPF válido a partir de base."""
    base_str = str(numero_base).zfill(9)

    # Calcular primeiro dígito
    soma = sum(int(base_str[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Calcular segundo dígito
    base_com_d1 = base_str + str(digito1)
    soma = sum(int(base_com_d1[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return base_str + str(digito1) + str(digito2)


@pytest.fixture
def repo():
    """Fixture com repositório limpo."""
    return UsuarioRepository()


@pytest.fixture
def usuario_padrao():
    """Fixture com usuário padrão."""
    return Usuario(
        nome="Werner Schindel",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP Expert IA",
        cargo="Desenvolvedor"
    )


def test_repository_salvar(repo, usuario_padrao):
    """Testa salvar um usuário."""
    resultado = repo.salvar(usuario_padrao)
    assert resultado.id is not None


def test_repository_buscar_por_id(repo, usuario_padrao):
    """Testa buscar usuário por ID."""
    repo.salvar(usuario_padrao)
    encontrado = repo.buscar_por_id(1)
    assert encontrado is not None
    assert encontrado.nome == "Werner Schindel"


def test_repository_buscar_por_email(repo, usuario_padrao):
    """Testa buscar usuário por email."""
    repo.salvar(usuario_padrao)
    encontrado = repo.buscar_por_email("werner@example.com")
    assert encontrado is not None
    assert encontrado.id == 1


def test_repository_buscar_por_cpf(repo, usuario_padrao):
    """Testa buscar usuário por CPF."""
    repo.salvar(usuario_padrao)
    encontrado = repo.buscar_por_cpf("111.444.777-35")
    assert encontrado is not None


def test_repository_listar_todos(repo, usuario_padrao):
    """Testa listar todos os usuários."""
    repo.salvar(usuario_padrao)
    repo.salvar(Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="Outra",
        cargo="Analista"
    ))
    todos = repo.listar_todos()
    assert len(todos) == 2


def test_repository_listar_ativos(repo, usuario_padrao):
    """Testa listar usuários ativos."""
    repo.salvar(usuario_padrao)
    usuario_padrao.desativar()

    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="Outra",
        cargo="Analista"
    )
    repo.salvar(usuario2)

    ativos = repo.listar_ativos()
    assert len(ativos) == 1


def test_repository_email_duplicado_falha(repo, usuario_padrao):
    """Testa que email duplicado falha."""
    repo.salvar(usuario_padrao)

    usuario2 = Usuario(
        nome="Outro",
        email=Email("werner@example.com"),  # Email duplicado
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="Outra",
        cargo="Analista"
    )

    with pytest.raises(ValueError):
        repo.salvar(usuario2)


def test_repository_cpf_duplicado_falha(repo, usuario_padrao):
    """Testa que CPF duplicado falha."""
    repo.salvar(usuario_padrao)

    usuario2 = Usuario(
        nome="Outro",
        email=Email("outro@example.com"),
        cpf=CPF("11144477735"),  # CPF duplicado
        empresa="Outra",
        cargo="Analista"
    )

    with pytest.raises(ValueError):
        repo.salvar(usuario2)
