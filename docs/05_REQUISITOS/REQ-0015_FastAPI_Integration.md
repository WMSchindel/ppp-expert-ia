---
documento: REQ-0015
titulo: Especificação Técnica — FastAPI Framework Integration
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 10/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-012
---

# Especificação Técnica

## Pacote

CF-012 — FastAPI Framework Integration

---

# Objetivo

Integrar FastAPI para servir REST API endpoints com validação automática e OpenAPI documentation.

---

# Stack

## FastAPI

**Versão:** 0.104+ (latest)

**Características:**
- Async/await support
- Automatic OpenAPI/Swagger
- Built-in validation (Pydantic)
- Dependency injection
- Type hints

## Uvicorn (ASGI Server)

**Versão:** latest

**Características:**
- High-performance async server
- Hot reload in development
- Multiple workers in production

## Pydantic (Models)

**Versão:** 2.0+ (already installed)

**Characteristics:**
- Request validation
- Response serialization
- JSON Schema generation

---

# Implementation Plan

## 1. FastAPI Application Setup

**File:** `src/main.py`

```python
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from src.infrastructure.persistence.database import SessionLocal, get_db
from src.core.logging import logger

app = FastAPI(
    title="PPP Expert IA",
    description="Sistema Inteligente para Elaboração de Perfil Profissiográfico Previdenciário",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application starting")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutting down")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}
```

## 2. Request/Response Models

**File:** `src/presentation/schemas/usuario_schemas.py`

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CriarUsuarioRequest(BaseModel):
    """Request to create usuario."""
    nome: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    cpf: str = Field(..., regex="^\d{11}$")
    empresa: str = Field(..., min_length=1, max_length=255)
    cargo: str = Field(..., min_length=1, max_length=255)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Werner",
                "email": "werner@example.com",
                "cpf": "11144477735",
                "empresa": "PPP",
                "cargo": "Dev"
            }
        }

class UsuarioResponse(BaseModel):
    """Response with usuario data."""
    id: int
    nome: str
    email: str
    empresa: str
    cargo: str
    ativo: bool
    data_criacao: datetime
    
    class Config:
        from_attributes = True

class CriarUsuarioResponse(BaseModel):
    """Response from create usuario."""
    sucesso: bool
    mensagem: str
    usuario_id: Optional[int] = None
```

## 3. FastAPI Routes

**File:** `src/presentation/routes/usuarios_routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories.usuario_repository_sql import UsuarioRepositorySQL
from src.presentation.controllers.usuario_controller import UsuarioController
from src.presentation.schemas.usuario_schemas import CriarUsuarioRequest, UsuarioResponse
from src.core.logging import logger

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])

def get_repository(db: Session = Depends(get_db)) -> UsuarioRepositorySQL:
    """Dependency injection for repository."""
    return UsuarioRepositorySQL(db)

def get_controller(repo: UsuarioRepositorySQL = Depends(get_repository)) -> UsuarioController:
    """Dependency injection for controller."""
    return UsuarioController(repo)

@router.post("/", status_code=201)
async def criar_usuario(
    dados: CriarUsuarioRequest,
    controller: UsuarioController = Depends(get_controller)
):
    """Create new usuario."""
    logger.info("POST /api/v1/usuarios", extra={"nome": dados.nome})
    
    resposta = controller.criar_usuario(dados.dict())
    
    if not resposta["sucesso"]:
        logger.warning("Falha ao criar usuario", extra={"mensagem": resposta["mensagem"]})
        raise HTTPException(status_code=400, detail=resposta["mensagem"])
    
    logger.info("Usuario criado", extra={"usuario_id": resposta["usuario_id"]})
    return {
        "sucesso": resposta["sucesso"],
        "mensagem": resposta["mensagem"],
        "usuario_id": resposta["usuario_id"]
    }

@router.get("/", status_code=200)
async def listar_usuarios(
    controller: UsuarioController = Depends(get_controller)
):
    """List all active usuarios."""
    logger.info("GET /api/v1/usuarios")
    
    resposta = controller.listar_usuarios()
    
    return {
        "sucesso": resposta["sucesso"],
        "mensagem": resposta["mensagem"],
        "usuarios": resposta["usuarios"]
    }

@router.put("/{usuario_id}/cargo", status_code=200)
async def atualizar_cargo(
    usuario_id: int,
    novo_cargo: str,
    controller: UsuarioController = Depends(get_controller)
):
    """Update usuario cargo."""
    logger.info(f"PUT /api/v1/usuarios/{usuario_id}/cargo")
    
    resposta = controller.atualizar_cargo(usuario_id, {"novo_cargo": novo_cargo})
    
    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])
    
    return resposta

@router.put("/{usuario_id}/empresa", status_code=200)
async def atualizar_empresa(
    usuario_id: int,
    nova_empresa: str,
    controller: UsuarioController = Depends(get_controller)
):
    """Update usuario empresa."""
    logger.info(f"PUT /api/v1/usuarios/{usuario_id}/empresa")
    
    resposta = controller.atualizar_empresa(usuario_id, {"nova_empresa": nova_empresa})
    
    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])
    
    return resposta

@router.delete("/{usuario_id}", status_code=200)
async def desativar_usuario(
    usuario_id: int,
    controller: UsuarioController = Depends(get_controller)
):
    """Deactivate usuario."""
    logger.info(f"DELETE /api/v1/usuarios/{usuario_id}")
    
    resposta = controller.desativar_usuario(usuario_id)
    
    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])
    
    return resposta
```

## 4. Update main.py with Routes

```python
from fastapi import FastAPI
from src.presentation.routes.usuarios_routes import router as usuarios_router

app = FastAPI(...)

# Include routers
app.include_router(usuarios_router)
```

## 5. Testing FastAPI Endpoints

**File:** `tests/integration/test_fastapi_endpoints.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.infrastructure.persistence.database import get_db, Base

@pytest.fixture
def db_engine():
    """Create in-memory SQLite for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db_engine):
    """Create database session."""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(db_session):
    """Create FastAPI test client."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_criar_usuario(client):
    """Test creating usuario via HTTP."""
    response = client.post("/api/v1/usuarios", json={
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": "11144477735",
        "empresa": "PPP",
        "cargo": "Dev"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["sucesso"] is True
    assert data["usuario_id"] is not None

def test_listar_usuarios_vazio(client):
    """Test listing when empty."""
    response = client.get("/api/v1/usuarios")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["usuarios"]) == 0

def test_criar_e_listar(client):
    """Test create then list."""
    # Create
    client.post("/api/v1/usuarios", json={
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": "11144477735",
        "empresa": "PPP",
        "cargo": "Dev"
    })
    
    # List
    response = client.get("/api/v1/usuarios")
    assert len(response.json()["usuarios"]) == 1

def test_atualizar_cargo(client):
    """Test updating cargo."""
    # Create
    create_resp = client.post("/api/v1/usuarios", json={
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": "11144477735",
        "empresa": "PPP",
        "cargo": "Dev"
    })
    usuario_id = create_resp.json()["usuario_id"]
    
    # Update
    response = client.put(
        f"/api/v1/usuarios/{usuario_id}/cargo",
        json={"novo_cargo": "Senior Dev"}
    )
    assert response.status_code == 200
    assert response.json()["sucesso"] is True
```

---

# Features

## Automatic OpenAPI Documentation

```bash
curl http://localhost:8000/docs
curl http://localhost:8000/redoc
```

## Automatic Validation

Pydantic validates:
- Email format
- CPF format (11 digits)
- Required fields
- String lengths

## Dependency Injection

```python
def criar_usuario(
    dados: CriarUsuarioRequest,
    controller: UsuarioController = Depends(get_controller)
):
    ...
```

FastAPI handles:
- Database session creation
- Repository instantiation
- Controller creation
- Cleanup

## Error Handling

```python
if not resposta["sucesso"]:
    raise HTTPException(status_code=400, detail=resposta["mensagem"])
```

Returns proper HTTP status codes + error messages.

---

# Running the Application

## Development

```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Run with hot reload
uvicorn src.main:app --reload

# Open browser
http://localhost:8000/docs
```

## Production

```bash
# Run with 4 workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app

# Or with Uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

# Tests

## Total New Tests

- 10+ FastAPI integration tests
- Test with TestClient
- Mock database with SQLite in-memory
- Test all 5 endpoints

Expected total: **150+** tests

---

# Deliverables

✅ FastAPI application (src/main.py)
✅ Request/Response schemas (Pydantic)
✅ Routes module with 5 endpoints
✅ Dependency injection setup
✅ 10+ integration tests
✅ OpenAPI documentation (automatic)
✅ Error handling

---

# Próxima Fase

CF-013 — Documentação Técnica Completa (Technical Docs)

