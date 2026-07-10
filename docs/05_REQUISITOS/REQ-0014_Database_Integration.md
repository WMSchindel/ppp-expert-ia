---
documento: REQ-0014
titulo: Especificação Técnica — Integração com Banco de Dados Real
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 10/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-011
---

# Especificação Técnica

## Pacote

CF-011 — Real Database Integration (SQLAlchemy + PostgreSQL)

---

# Objetivo

Substituir UsuarioRepository in-memory por implementação real com SQLAlchemy + PostgreSQL.

---

# Stack Database

## SQLAlchemy ORM

**Versão:** 2.0+ (latest)

**Características:**
- Declarative ORM
- Type hints support
- Async support
- Query builder

## PostgreSQL

**Versão:** 16 (latest)

**Características:**
- JSONB support
- Full-text search
- Transactions
- Indexes

## Alembic (Migrations)

**Versão:** latest

**Características:**
- Schema versioning
- Rollback support
- Downtime-free migrations

---

# Implementation Plan

## 1. Database Models (SQLAlchemy)

### Create ORM Models

**File:** `src/infrastructure/persistence/models/usuario_model.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    empresa = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_entity(self) -> Usuario:
        """Convert ORM model to domain entity."""
        usuario = Usuario(
            nome=self.nome,
            email=Email(self.email),
            cpf=CPF(self.cpf),
            empresa=self.empresa,
            cargo=self.cargo
        )
        usuario.id = self.id
        usuario.ativo = self.ativo
        usuario.data_criacao = self.data_criacao
        return usuario
```

## 2. Database Connection

### Create Database Session

**File:** `src/infrastructure/persistence/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

DATABASE_URL = settings.database_url  # from .env

engine = create_engine(
    DATABASE_URL,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.debug  # Log SQL queries in development
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency injection for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 3. SQLAlchemy Repository

### Create UsuarioRepositorySQL

**File:** `src/infrastructure/persistence/repositories/usuario_repository_sql.py`

```python
from sqlalchemy.orm import Session
from src.domain.entities.usuario import Usuario
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository
from src.infrastructure.persistence.models.usuario_model import UsuarioModel
from src.core.logging import logger

class UsuarioRepositorySQL(UsuarioRepository):
    """SQLAlchemy implementation of UsuarioRepository."""
    
    def __init__(self, db: Session):
        self.db = db
        logger.info("UsuarioRepositorySQL initialized")
    
    def salvar(self, usuario: Usuario) -> None:
        """Save usuario to database."""
        logger.info("Saving usuario", extra={"email": usuario.email.valor})
        
        # Check email uniqueness
        if self._existe_email(usuario.email):
            logger.warning("Email already exists", extra={"email": usuario.email.valor})
            raise ValueError("Email já existe")
        
        # Check CPF uniqueness
        if self._existe_cpf(usuario.cpf):
            logger.warning("CPF already exists", extra={"cpf": usuario.cpf.valor})
            raise ValueError("CPF já existe")
        
        # Create model and save
        model = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email.valor,
            cpf=usuario.cpf.valor,
            empresa=usuario.empresa,
            cargo=usuario.cargo,
            ativo=usuario.ativo
        )
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        usuario.id = model.id
        logger.info("Usuario saved", extra={"usuario_id": usuario.id})
    
    def buscar_por_id(self, id: int) -> Usuario | None:
        """Fetch usuario by ID."""
        logger.debug("Fetching usuario by ID", extra={"id": id})
        
        model = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        
        if not model:
            logger.debug("Usuario not found", extra={"id": id})
            return None
        
        return model.to_entity()
    
    def buscar_por_email(self, email: Email) -> Usuario | None:
        """Fetch usuario by email."""
        model = self.db.query(UsuarioModel).filter(
            UsuarioModel.email == email.valor
        ).first()
        
        return model.to_entity() if model else None
    
    def buscar_por_cpf(self, cpf: CPF) -> Usuario | None:
        """Fetch usuario by CPF."""
        model = self.db.query(UsuarioModel).filter(
            UsuarioModel.cpf == cpf.valor
        ).first()
        
        return model.to_entity() if model else None
    
    def listar_todos(self) -> list[Usuario]:
        """List all usuarios."""
        models = self.db.query(UsuarioModel).all()
        return [model.to_entity() for model in models]
    
    def listar_ativos(self) -> list[Usuario]:
        """List only active usuarios."""
        models = self.db.query(UsuarioModel).filter(
            UsuarioModel.ativo == True
        ).all()
        return [model.to_entity() for model in models]
    
    def deletar(self, id: int) -> None:
        """Delete usuario by ID."""
        self.db.query(UsuarioModel).filter(UsuarioModel.id == id).delete()
        self.db.commit()
    
    def contar(self) -> int:
        """Count total usuarios."""
        return self.db.query(UsuarioModel).count()
    
    def _existe_email(self, email: Email) -> bool:
        """Check if email exists."""
        return self.db.query(UsuarioModel).filter(
            UsuarioModel.email == email.valor
        ).first() is not None
    
    def _existe_cpf(self, cpf: CPF) -> bool:
        """Check if CPF exists."""
        return self.db.query(UsuarioModel).filter(
            UsuarioModel.cpf == cpf.valor
        ).first() is not None
```

## 4. Database Migrations (Alembic)

### Setup Alembic

```bash
alembic init alembic
```

### Create Initial Migration

**File:** `alembic/env.py` (configure)

**File:** `alembic/versions/001_create_usuarios_table.py`

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('cpf', sa.String(11), unique=True, nullable=False),
        sa.Column('empresa', sa.String(255), nullable=False),
        sa.Column('cargo', sa.String(255), nullable=False),
        sa.Column('ativo', sa.Boolean, default=True, nullable=False),
        sa.Column('data_criacao', sa.DateTime, server_default=sa.func.now()),
    )
    
    op.create_index('ix_usuarios_email', 'usuarios', ['email'])
    op.create_index('ix_usuarios_cpf', 'usuarios', ['cpf'])

def downgrade():
    op.drop_table('usuarios')
```

### Run Migrations

```bash
alembic upgrade head
```

---

## 5. Configuration Updates

### Update Settings

**File:** `src/core/config/settings.py`

Add database configuration:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Previous config...
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ppp_db"
    database_pool_size: int = 20
    database_max_overflow: int = 40
    
    class Config:
        env_file = ".env"
```

### Update .env Files

**.env.test**
```bash
DATABASE_URL=sqlite:///test.db
```

**.env.local**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/ppp_dev
```

**.env.production**
```bash
DATABASE_URL=postgresql://user:securepassword@db-prod:5432/ppp_prod
```

---

## 6. Testing Strategy

### Test Setup

**File:** `tests/conftest.py` (update)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.persistence.database import Base
from src.infrastructure.persistence.repositories.usuario_repository_sql import UsuarioRepositorySQL

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
def repository_sql(db_session):
    """Create SQL repository for testing."""
    return UsuarioRepositorySQL(db_session)
```

### Test Suite

**File:** `tests/unit/infrastructure/test_usuario_repository_sql.py`

```python
def test_salvar_usuario(repository_sql):
    """Test saving usuario to database."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    
    repository_sql.salvar(usuario)
    
    assert usuario.id is not None
    assert repository_sql.buscar_por_id(usuario.id) is not None

def test_email_uniqueness(repository_sql):
    """Test email uniqueness constraint."""
    usuario1 = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF(gerar_cpf_valido(111444777)),
        empresa="PPP",
        cargo="Dev"
    )
    
    usuario2 = Usuario(
        nome="João",
        email=Email("werner@example.com"),  # Duplicate!
        cpf=CPF(gerar_cpf_valido(214741688)),
        empresa="PPP",
        cargo="Dev"
    )
    
    repository_sql.salvar(usuario1)
    
    with pytest.raises(ValueError, match="Email já existe"):
        repository_sql.salvar(usuario2)
```

---

## 7. Docker Setup (Optional)

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ppp_user
      POSTGRES_PASSWORD: ppp_password
      POSTGRES_DB: ppp_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ppp_user:ppp_password@postgres:5432/ppp_db
    depends_on:
      - postgres

volumes:
  postgres_data:
```

### Run with Docker

```bash
docker-compose up -d
alembic upgrade head
```

---

# Migration Path

## From In-Memory to SQL

The beauty of Repository pattern:

```python
# Phase 1: In-memory (current)
repo = UsuarioRepository()

# Phase 2: SQL (CF-011)
db_session = SessionLocal()
repo = UsuarioRepositorySQL(db_session)

# UseCase stays EXACTLY THE SAME
case = CriarUsuarioUseCase(repo)
resposta = case(requisicao)
```

**No changes needed to UseCase, Controller, or Tests!**

---

# Tests

## Total New Tests

- 15+ integration tests with real database
- All existing 129 tests still passing
- Expected: 145+ tests total

## Test Types

- Unit tests (in-memory)
- Integration tests (real database)
- E2E tests (full stack)

---

# Deliverables

✅ SQLAlchemy ORM models
✅ UsuarioRepositorySQL implementation
✅ Alembic migrations
✅ Database configuration
✅ Docker setup
✅ Test fixtures
✅ 15+ new tests
✅ Documentation

---

# Próxima Fase

CF-012 — FastAPI Framework Integration

