"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.infrastructure.persistence.database import get_db, Base


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
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=None,  # Disable connection pooling for in-memory SQLite
    )
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
def client(db_engine, db_session):
    """Create FastAPI test client with test database."""
    # Ensure tables are created
    Base.metadata.create_all(bind=db_engine)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


# HEALTH CHECK TESTS
def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


# CREATE USUARIO TESTS
def test_criar_usuario_sucesso(client):
    """Test creating usuario via HTTP."""
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["sucesso"] is True
    assert data["usuario_id"] is not None
    assert data["mensagem"] is not None


def test_criar_usuario_email_invalido(client):
    """Test creating usuario with invalid email."""
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "invalido",  # Invalid email
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    assert response.status_code == 422  # Validation error


def test_criar_usuario_cpf_invalido(client):
    """Test creating usuario with invalid CPF."""
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": "12345",  # Invalid CPF (not 11 digits)
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    assert response.status_code == 422  # Validation error


def test_criar_usuario_nome_vazio(client):
    """Test creating usuario with empty name."""
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "",  # Empty
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    assert response.status_code == 422  # Validation error


def test_criar_usuario_email_duplicado(client):
    """Test creating usuario with duplicate email."""
    # Create first usuario
    client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    # Try to create with same email
    response = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "João",
            "email": "werner@example.com",  # Duplicate!
            "cpf": gerar_cpf_valido(214741688),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    assert response.status_code == 400
    data = response.json()
    assert "Email" in data["detail"]


# LISTAR TESTS
def test_listar_usuarios_vazio(client):
    """Test listing usuarios when empty."""
    response = client.get("/api/v1/usuarios")

    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True
    assert len(data["usuarios"]) == 0


def test_listar_usuarios_com_dados(client):
    """Test listing usuarios with data."""
    # Create usuario
    client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    # List
    response = client.get("/api/v1/usuarios")

    assert response.status_code == 200
    data = response.json()
    assert len(data["usuarios"]) == 1
    assert data["usuarios"][0]["nome"] == "Werner"


def test_criar_e_listar_multiplos(client):
    """Test creating multiple usuarios and listing."""
    # Create usuario 1
    client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )

    # Create usuario 2
    client.post(
        "/api/v1/usuarios",
        json={
            "nome": "João",
            "email": "joao@example.com",
            "cpf": gerar_cpf_valido(214741688),
            "empresa": "PPP",
            "cargo": "Analista",
        },
    )

    # List
    response = client.get("/api/v1/usuarios")

    assert response.status_code == 200
    data = response.json()
    assert len(data["usuarios"]) == 2


# ATUALIZAR TESTS
def test_atualizar_cargo_sucesso(client):
    """Test updating usuario cargo via HTTP."""
    # Create
    create_resp = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )
    usuario_id = create_resp.json()["usuario_id"]

    # Update
    response = client.put(
        f"/api/v1/usuarios/{usuario_id}/cargo?novo_cargo=Senior%20Dev"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True


def test_atualizar_empresa_sucesso(client):
    """Test updating usuario empresa via HTTP."""
    # Create
    create_resp = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "Empresa A",
            "cargo": "Dev",
        },
    )
    usuario_id = create_resp.json()["usuario_id"]

    # Update
    response = client.put(
        f"/api/v1/usuarios/{usuario_id}/empresa?nova_empresa=Empresa%20B"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True


# DESATIVAR TESTS
def test_desativar_usuario(client):
    """Test deactivating usuario via HTTP."""
    # Create
    create_resp = client.post(
        "/api/v1/usuarios",
        json={
            "nome": "Werner",
            "email": "werner@example.com",
            "cpf": gerar_cpf_valido(111444777),
            "empresa": "PPP",
            "cargo": "Dev",
        },
    )
    usuario_id = create_resp.json()["usuario_id"]

    # Delete (deactivate)
    response = client.delete(f"/api/v1/usuarios/{usuario_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["sucesso"] is True

    # Verify not in list
    list_resp = client.get("/api/v1/usuarios")
    assert len(list_resp.json()["usuarios"]) == 0


# OPENAPI TESTS
def test_openapi_docs_available(client):
    """Test that OpenAPI docs are available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_available(client):
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "/api/v1/usuarios" in data["paths"]
