# Architecture

PPP Expert IA — System Architecture & Design

---

## Quick Start

**Current State:**
- 129 tests passing (100%)
- 5-layer Clean Architecture
- 1 entity: Usuario
- 5 use cases
- RESTful controller ready

**Stack:**
- Python 3.13
- Pydantic v2 (validation & settings)
- Loguru (logging)
- Pytest (testing)

---

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Client / Browser                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Controllers)                │
│  Coordinate HTTP requests to business logic            │
│  - UsuarioController (5 endpoints)                     │
└────────────────────────┬────────────────────────────────┘
                         │ UseCase Call
                         ▼
┌─────────────────────────────────────────────────────────┐
│        APPLICATION LAYER (Use Cases)                    │
│  Orchestrate business logic flows                      │
│  - CriarUsuarioUseCase                                │
│  - AtualizarCargoUseCase                              │
│  - AtualizarEmpresaUseCase                            │
│  - DesativarUsuarioUseCase                            │
│  - ListarUsuariosAtivosUseCase                        │
└────────────────────────┬────────────────────────────────┘
                         │ Domain Operation
                         ▼
┌─────────────────────────────────────────────────────────┐
│          DOMAIN LAYER (Business Rules)                  │
│  Represent pure business logic, independent of tech    │
│  - Usuario (Entity)                                    │
│  - Email (ValueObject)                                │
│  - CPF (ValueObject)                                  │
└────────────────────────┬────────────────────────────────┘
                         │ Repository Call
                         ▼
┌─────────────────────────────────────────────────────────┐
│      INFRASTRUCTURE LAYER (Persistence)                 │
│  Handle data persistence and external systems         │
│  - UsuarioRepository (in-memory for now)              │
│  - Uniqueness constraint enforcement                  │
└────────────────────────┬────────────────────────────────┘
                         │ Data Storage
                         ▼
┌─────────────────────────────────────────────────────────┐
│        CORE LAYER (Shared Services)                     │
│  Global configuration and logging                      │
│  - Logger (Loguru singleton)                          │
│  - Settings (Pydantic v2)                            │
│  - Environment configuration                          │
└─────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Presentation Layer
**File:** `src/presentation/controllers/usuario_controller.py`

Converts HTTP requests to UseCase calls and responses.

```python
def criar_usuario(self, dados: dict) -> dict:
    """POST /api/v1/usuarios"""
    requisicao = CriarUsuarioRequest(**dados)
    resposta = self.criar_caso(requisicao)
    return {"sucesso": resposta.sucesso, "usuario_id": resposta.usuario_id}
```

**Responsibilities:**
- Parse HTTP input
- Call appropriate UseCase
- Format HTTP response
- Logging at entry point

**Does NOT:**
- Do business logic
- Access database directly
- Know about repositories

---

### Application Layer
**File:** `src/application/use_cases/usuario_use_cases.py`

Orchestrates business logic using domain objects.

```python
class CriarUsuarioUseCase(UseCase):
    def executar(self, requisicao: CriarUsuarioRequest) -> CriarUsuarioResponse:
        # Create Email ValueObject (validates format)
        email = Email(requisicao.email)
        
        # Create CPF ValueObject (validates checksum)
        cpf = CPF(requisicao.cpf)
        
        # Create Usuario Entity
        usuario = Usuario(
            nome=requisicao.nome,
            email=email,
            cpf=cpf,
            empresa=requisicao.empresa,
            cargo=requisicao.cargo
        )
        
        # Persist via Repository
        self.repository.salvar(usuario)
        
        return CriarUsuarioResponse(
            sucesso=True,
            usuario_id=usuario.id
        )
```

**Responsibilities:**
- Orchestrate business flows
- Create domain objects
- Call repository operations
- Return structured responses

**Does NOT:**
- Know about HTTP
- Directly access database
- Enforce business rules (that's domain's job)

---

### Domain Layer
**Files:**
- `src/domain/entities/usuario.py`
- `src/domain/value_objects/email.py`
- `src/domain/value_objects/cpf.py`

Pure business logic independent of technology.

```python
class Email(ValueObject):
    """Email with validation."""
    def __init__(self, valor: str):
        if "@" not in valor or "." not in valor.split("@")[1]:
            raise ValueError("Invalid email format")
        self._valor = valor.lower()  # Normalize

class Usuario(Entity):
    """User in the system."""
    def __init__(self, nome: str, email: Email, cpf: CPF, ...):
        self.id = None  # Set by Repository
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.ativo = True
        self.data_criacao = datetime.now()
```

**Responsibilities:**
- Define entities (Usuario)
- Define value objects (Email, CPF)
- Enforce business rules (Email format, CPF checksum)
- Represent pure logic

**Does NOT:**
- Know about HTTP
- Access database
- Know about repositories
- Do I/O operations

---

### Infrastructure Layer
**File:** `src/infrastructure/persistence/repositories/usuario_repository.py`

Abstracts data persistence.

```python
class UsuarioRepository(Repository[Usuario]):
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}
        self._proximo_id = 1
    
    def salvar(self, usuario: Usuario) -> None:
        # Validate uniqueness BEFORE inserting
        if self._existe_email(usuario.email):
            raise ValueError("Email já existe")
        if self._existe_cpf(usuario.cpf):
            raise ValueError("CPF já existe")
        
        # Assign ID if new
        if usuario.id is None:
            usuario.id = self._proximo_id
            self._proximo_id += 1
        
        # Store
        self._usuarios[usuario.id] = usuario
```

**Responsibilities:**
- Persist domain objects
- Retrieve domain objects
- Enforce uniqueness constraints
- Abstract storage backend

**Does NOT:**
- Do business logic
- Know about HTTP
- Know about UseCases

---

### Core Layer
**Files:**
- `src/core/logging/logger.py`
- `src/core/config/settings.py`
- `src/core/config/environments.py`
- `src/core/config/defaults.py`

Global services and configuration.

```python
# Logger (Loguru singleton)
logger.info("Usuario criado", extra={"usuario_id": usuario.id})

# Settings (Pydantic v2)
settings = Settings()
print(settings.logs_path)  # project_root/data/logs
```

**Responsibilities:**
- Configure application
- Provide logging
- Manage environment variables
- Store defaults

**Used by:** All layers

---

## Design Patterns

### 1. Clean Architecture

Dependency rule: Dependencies point inward (toward Domain).

```
Presentation ──→ Application ──→ Domain ←── Infrastructure
                                    ↑
                                   Core
```

**Benefit:** Domain logic never depends on web/database frameworks.

### 2. Repository Pattern

Abstract persistence behind interface.

```
UseCase → Repository (abstract)
           ↓
           UsuarioRepository (in-memory)
           ↓ (future)
           UsuarioRepositorySQL (PostgreSQL)
```

**Benefit:** Swap implementations without changing UseCase.

### 3. Entity Pattern

Objects with identity and lifecycle.

```python
class Usuario(Entity):
    id: int
    nome: str
    email: Email
    cpf: CPF
    ativo: bool
    data_criacao: datetime
    
    def desativar(self) -> None:
        self.ativo = False
```

**Benefit:** Entities maintain their own invariants.

### 4. ValueObject Pattern

Immutable objects without identity.

```python
class Email(ValueObject):
    # Two emails with same address are equal
    email1 = Email("werner@example.com")
    email2 = Email("werner@example.com")
    assert email1 == email2  # True (no ID comparison)
```

**Benefit:** Type-safe, immutable, validation at construction.

### 5. UseCase Pattern

Explicit input/output contracts.

```python
class CriarUsuarioUseCase:
    def executar(self, requisicao: CriarUsuarioRequest) -> CriarUsuarioResponse:
        ...

@dataclass
class CriarUsuarioRequest:
    nome: str
    email: str
    cpf: str
    empresa: str
    cargo: str

@dataclass
class CriarUsuarioResponse:
    sucesso: bool
    mensagem: str
    usuario_id: int | None = None
```

**Benefit:** Clear contracts, testable, type-safe.

### 6. Singleton Pattern (Logger & Settings)

Single global instance per service.

```python
from src.core.logging import logger
logger.info("Something happened")

from src.core.config import settings
print(settings.environment)  # "development"
```

**Benefit:** Single source of truth, easy access.

---

## Data Flow Example

### Create User Flow

```
1. HTTP POST /api/v1/usuarios
   {
     "nome": "Werner",
     "email": "werner@example.com",
     "cpf": "111.444.777-35",
     "empresa": "PPP",
     "cargo": "Dev"
   }

2. Controller.criar_usuario()
   - Parse request data
   - Create CriarUsuarioRequest dataclass
   - Call CriarUsuarioUseCase

3. CriarUsuarioUseCase.executar()
   - Create Email ValueObject (validates format)
   - Create CPF ValueObject (validates checksum)
   - Create Usuario Entity
   - Call Repository.salvar()

4. Repository.salvar()
   - Check email uniqueness
   - Check CPF uniqueness
   - Assign ID
   - Store in memory

5. Response
   {
     "sucesso": true,
     "mensagem": "Usuario criado",
     "usuario_id": 1
   }

6. HTTP 201 Created
```

---

## Testing Strategy

### Unit Tests (122 tests)
Test individual components in isolation.

```python
# Test ValueObject
def test_email_invalido():
    with pytest.raises(ValueError):
        Email("invalid")

# Test Entity
def test_usuario_pode_ser_criado():
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF("111.444.777-35"),
        empresa="PPP",
        cargo="Dev"
    )
    assert usuario.nome == "Werner"

# Test UseCase
def test_criar_usuario_sucesso():
    repo = UsuarioRepository()
    caso = CriarUsuarioUseCase(repo)
    resposta = caso(CriarUsuarioRequest(...))
    assert resposta.sucesso
```

### Integration Tests (7 E2E tests)
Test full flows end-to-end.

```python
# E2E: Create and list
def test_e2e_criar_e_listar():
    controller = UsuarioController(UsuarioRepository())
    
    # Create
    resposta_criar = controller.criar_usuario({...})
    assert resposta_criar["sucesso"]
    
    # List
    resposta_listar = controller.listar_usuarios()
    assert len(resposta_listar["usuarios"]) == 1
```

---

## Directory Structure

```
ppp-expert-ia/
├── src/
│   ├── core/
│   │   ├── logging/
│   │   │   └── logger.py              # Loguru singleton
│   │   └── config/
│   │       ├── settings.py            # Pydantic Settings
│   │       ├── defaults.py            # Default constants
│   │       └── environments.py        # Environment enum
│   │
│   ├── domain/
│   │   ├── entities/
│   │   │   └── usuario.py             # Usuario Entity
│   │   └── value_objects/
│   │       ├── email.py               # Email ValueObject
│   │       └── cpf.py                 # CPF ValueObject
│   │
│   ├── application/
│   │   └── use_cases/
│   │       └── usuario_use_cases.py   # 5 UseCases
│   │
│   ├── infrastructure/
│   │   └── persistence/
│   │       └── repositories/
│   │           └── usuario_repository.py  # UsuarioRepository
│   │
│   └── presentation/
│       └── controllers/
│           └── usuario_controller.py  # UsuarioController
│
├── tests/
│   ├── unit/                          # 122 unit tests
│   │   ├── core/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   │
│   └── integration/
│       └── test_usuario_e2e.py        # 7 E2E tests
│
├── docs/
│   ├── ARCH.md                        # This file
│   ├── DECISIONS.md                   # Architecture decisions
│   ├── TRADEOFFS.md                   # Design trade-offs
│   ├── DEPLOYMENT.md                  # Deployment strategy
│   ├── SCALABILITY.md                 # Future scalability
│   └── 05_REQUISITOS/
│       └── REQ-0013_Architecture_Documentation.md
│
├── pyproject.toml                     # Project configuration
├── conftest.py                        # Pytest configuration
└── README.md                          # Project overview
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Tests Passing | 129/129 (100%) |
| Test Execution Time | ~0.46s |
| Entities | 1 (Usuario) |
| Value Objects | 2 (Email, CPF) |
| Use Cases | 5 |
| Repositories | 1 |
| Controllers | 1 |
| Endpoints | 5 |
| Lines of Code | ~6000 |

---

## Next Steps

### CF-011: Real Database
- SQLAlchemy ORM
- PostgreSQL integration
- Database migrations

### CF-012: HTTP Framework
- FastAPI integration
- OpenAPI/Swagger
- Validation middleware

### CF-013+: More Entities
- Scale to multiple domains
- Reuse patterns
- Complex business logic

---

## Learning Resources

- **Clean Architecture:** Robert C. Martin "Clean Architecture" book
- **Domain-Driven Design:** Eric Evans "Domain-Driven Design" book
- **Repository Pattern:** Patterns of Enterprise Application Architecture
- **Pydantic:** https://docs.pydantic.dev
- **Loguru:** https://loguru.readthedocs.io

---

**Status:** ✅ Current architecture stable and tested
