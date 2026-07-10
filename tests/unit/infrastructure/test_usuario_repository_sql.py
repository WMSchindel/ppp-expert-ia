"""Tests for UsuarioRepositorySQL."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.domain.entities.usuario import Usuario
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.infrastructure.persistence.models.usuario_model import Base, UsuarioModel
from src.infrastructure.persistence.repositories.usuario_repository_sql import (
    UsuarioRepositorySQL,
)


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
def db_engine():
    """Create in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    """Create database session for testing."""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def repository(db_session):
    """Create SQL repository for testing."""
    return UsuarioRepositorySQL(db_session)


# SALVAR TESTS
def test_salvar_usuario_novo(repository):
    """Test saving new usuario to database."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )

    repository.salvar(usuario)

    assert usuario.id is not None
    assert usuario.id > 0


def test_salvar_usuario_atribui_id(repository, db_session):
    """Test that saving usuario assigns an ID."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )

    assert usuario.id is None
    repository.salvar(usuario)
    assert usuario.id is not None

    # Verify in database
    model = db_session.query(UsuarioModel).filter_by(id=usuario.id).first()
    assert model is not None
    assert model.nome == "Werner"


def test_salvar_usuario_email_duplicado(repository):
    """Test that duplicate email raises error."""
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("werner@example.com"),  # Duplicate!
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Dev",
    )

    repository.salvar(usuario1)

    with pytest.raises(ValueError, match="Email já existe"):
        repository.salvar(usuario2)


def test_salvar_usuario_cpf_duplicado(repository):
    """Test that duplicate CPF raises error."""
    cpf = gerar_cpf_valido(111444777)
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(cpf),
        empresa="PPP",
        cargo="Dev",
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(cpf),  # Duplicate!
        empresa="PPP",
        cargo="Dev",
    )

    repository.salvar(usuario1)

    with pytest.raises(ValueError, match="CPF já existe"):
        repository.salvar(usuario2)


# BUSCAR TESTS
def test_buscar_por_id(repository):
    """Test fetching usuario by ID."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    repository.salvar(usuario)

    fetched = repository.buscar_por_id(usuario.id)

    assert fetched is not None
    assert fetched.nome == "Werner"
    assert fetched.email.valor == "werner@example.com"


def test_buscar_por_id_nao_existe(repository):
    """Test fetching non-existent usuario returns None."""
    result = repository.buscar_por_id(999)
    assert result is None


def test_buscar_por_email(repository):
    """Test fetching usuario by email."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    repository.salvar(usuario)

    email = Email("werner@example.com")
    fetched = repository.buscar_por_email(email)

    assert fetched is not None
    assert fetched.nome == "Werner"


def test_buscar_por_cpf(repository):
    """Test fetching usuario by CPF."""
    cpf_str = gerar_cpf_valido(111444777)
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(cpf_str),
        empresa="PPP",
        cargo="Dev",
    )
    repository.salvar(usuario)

    cpf = CPF(cpf_str)
    fetched = repository.buscar_por_cpf(cpf)

    assert fetched is not None
    assert fetched.nome == "Werner"


# LISTAR TESTS
def test_listar_todos_vazio(repository):
    """Test listing usuarios when empty."""
    usuarios = repository.listar_todos()
    assert len(usuarios) == 0


def test_listar_todos(repository):
    """Test listing all usuarios."""
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Analista",
    )

    repository.salvar(usuario1)
    repository.salvar(usuario2)

    usuarios = repository.listar_todos()
    assert len(usuarios) == 2


def test_listar_ativos(repository):
    """Test listing only active usuarios."""
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Analista",
    )

    repository.salvar(usuario1)
    repository.salvar(usuario2)

    # Deactivate usuario2
    usuario2.desativar()
    repository.deletar(usuario2.id)  # Note: deletar actually sets ativo=False in SQL

    ativos = repository.listar_ativos()
    assert len(ativos) == 1
    assert ativos[0].nome == "Werner"


# DELETAR TESTS
def test_deletar_usuario(repository, db_session):
    """Test deleting usuario."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    repository.salvar(usuario)
    usuario_id = usuario.id

    repository.deletar(usuario_id)

    # Verify deleted
    model = db_session.query(UsuarioModel).filter_by(id=usuario_id).first()
    assert model is None


# CONTAR TESTS
def test_contar_usuarios_vazio(repository):
    """Test counting usuarios when empty."""
    count = repository.contar()
    assert count == 0


def test_contar_usuarios(repository):
    """Test counting usuarios."""
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev",
    )
    usuario2 = Usuario(
        nome="João",
        email=Email("joao@example.com"),
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Analista",
    )

    repository.salvar(usuario1)
    repository.salvar(usuario2)

    count = repository.contar()
    assert count == 2
