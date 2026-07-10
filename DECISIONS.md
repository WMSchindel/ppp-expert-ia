# Architecture Decision Records (ADRs)

Rationale behind key architectural decisions.

---

## ADR-001: Five-Layer Clean Architecture

**Status:** ACCEPTED ✅

**Decision:**
Organize application into 5 layers:
1. **Presentation** — HTTP/REST interface
2. **Application** — Use cases & business orchestration
3. **Domain** — Pure business logic & entities
4. **Infrastructure** — Data persistence & external services
5. **Core** — Shared services (logging, configuration)

**Rationale:**
- Clear separation of concerns
- Each layer has single responsibility
- Domain logic independent of web/database frameworks
- Easy to test layers in isolation
- Easy to swap implementations (e.g., in-memory → database)

**Alternatives Considered:**

1. **Hexagonal Architecture**
   - Similar goals but structured differently
   - Rejected: Less familiar to team, similar outcomes

2. **Single-Layer Monolith**
   - Simpler initially, all code in one place
   - Rejected: Harder to test, harder to scale

3. **Microservices**
   - Each domain becomes separate service
   - Rejected: Overkill for current project size

**Consequences:**
- ✅ Testability: Each layer tested independently
- ✅ Maintainability: Changes isolated to layer
- ✅ Scalability: Easy to add new entities
- ❌ More files: ~25 files for one entity
- ❌ Initial setup: More boilerplate

**When to Revisit:**
If project becomes too simple (fewer than 3 entities) or too complex (needs microservices).

---

## ADR-002: Singleton Pattern for Logger and Settings

**Status:** ACCEPTED ✅

**Decision:**
Logger and Settings are global singletons, not dependency-injected.

```python
# Instead of this (dependency injection):
class UserController:
    def __init__(self, logger: Logger, settings: Settings):
        self.logger = logger
        self.settings = settings

# We do this (singleton):
class UserController:
    def create(self):
        logger.info("Creating user")  # Direct access
        settings.get("APP_NAME")      # Direct access
```

**Rationale:**
- Logger and Settings are truly global concerns
- Every component needs access → DI becomes verbose
- Single source of truth for configuration
- Used by infrastructure (logging, DB config)
- Used by domain (for logging invariant violations)

**Alternatives Considered:**

1. **Full Dependency Injection**
   - Pass Logger/Settings to every constructor
   - Pro: More testable, explicit dependencies
   - Con: Verbose, 100+ parameters in chains
   - Rejected: Too much boilerplate

2. **No Logging**
   - Remove logging entirely
   - Pro: Simpler code
   - Con: Can't debug in production
   - Rejected: Not acceptable

3. **Lazy Initialization**
   - Load on first use
   - Pro: Avoids circular imports
   - Con: Slightly slower first access
   - Accepted as compromise: logger imported inside functions when needed

**Consequences:**
- ✅ Easy access from anywhere
- ✅ No verbose parameter passing
- ❌ Harder to test in complete isolation
- ❌ Global state (watch for side effects)

**Testing Strategy:**
- Reset logger state between tests (handled by pytest)
- Use fixtures to control settings during tests
- E2E tests validate actual logger behavior

**When to Revisit:**
If testing becomes difficult or need multiple logger instances.

---

## ADR-003: Repository Pattern for Persistence

**Status:** ACCEPTED ✅

**Decision:**
Abstract database access behind Repository interface.

```python
# Repository interface
class Repository(Generic[T]):
    def salvar(self, objeto: T) -> None: ...
    def buscar_por_id(self, id: int) -> T: ...
    def listar_todos(self) -> list[T]: ...
    def deletar(self, id: int) -> None: ...

# In-memory implementation for testing
class UsuarioRepository(Repository[Usuario]):
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}

# SQL implementation for production (future)
class UsuarioRepositorySQL(Repository[Usuario]):
    def __init__(self, db_session):
        self.db = db_session
```

**Rationale:**
- Decouple UseCase from specific database technology
- Tests run without database
- Easy to swap implementations
- Enforce persistence abstraction
- Validate operations at repository level

**Alternatives Considered:**

1. **Direct Database in UseCase**
   - Access database directly in business logic
   - Pro: Simpler
   - Con: Hard to test, tied to specific DB
   - Rejected: Violates layering

2. **ORM in UseCase**
   - Use SQLAlchemy directly in business logic
   - Pro: Less abstraction
   - Con: Still tied to ORM, hard to test
   - Rejected: Leaks technology into business logic

3. **Query Builder Pattern**
   - Pass query builders instead of objects
   - Pro: More flexible
   - Con: More complex, harder to understand
   - Rejected: Overkill for current needs

**Consequences:**
- ✅ Tests fast (in-memory)
- ✅ Can swap to real DB later
- ✅ Business logic independent of persistence
- ❌ Extra abstraction layer
- ❌ Uniqueness constraints must be enforced

**How Uniqueness is Enforced:**
Repository.salvar() validates email/CPF uniqueness:
```python
def salvar(self, usuario: Usuario) -> None:
    if self._existe_email(usuario.email):
        raise ValueError("Email já existe")
    if self._existe_cpf(usuario.cpf):
        raise ValueError("CPF já existe")
    # ... insert ...
```

**Future Phases:**
- Phase 1: In-memory (current) ✅
- Phase 2: SQLAlchemy + PostgreSQL (CF-011)
- Phase 3: Caching layer
- Phase 4: Read-Write separation (CQRS)

---

## ADR-004: ValueObject Pattern for Email and CPF

**Status:** ACCEPTED ✅

**Decision:**
Validation and immutability encapsulated in ValueObject classes.

```python
class Email(ValueObject):
    def __init__(self, valor: str):
        if "@" not in valor:
            raise ValueError("Email inválido")
        self._valor = valor.lower()
    
    @property
    def valor(self) -> str:
        return self._valor
    
    def __hash__(self):
        return hash(self._valor)
    
    def __eq__(self, other):
        return self._valor == other._valor

# Usage
email = Email("werner@example.com")  # Valid
email = Email("invalid")  # Raises ValueError immediately
email.valor = "new@example.com"  # Error: can't set attribute (immutable)
```

**Rationale:**
- Validation at construction time (fail fast)
- Type safety: Email type signals "validated"
- Immutability prevents accidental changes
- Equality by value (not identity)
- Hashable for sets/dict keys

**Alternatives Considered:**

1. **String Types with UseCase Validation**
   ```python
   class CriarUsuario:
       def validar_email(self, email: str) -> bool: ...
   ```
   - Pro: Less code
   - Con: Can create Usuario with invalid email
   - Rejected: Domain model can be in invalid state

2. **Dataclass with @frozen**
   ```python
   @dataclass(frozen=True)
   class Email:
       valor: str
   ```
   - Pro: Less code
   - Con: No validation at construction
   - Rejected: Can't prevent invalid emails

3. **String with Pydantic Field Validator**
   ```python
   class CriarUsuarioRequest(BaseModel):
       email: EmailStr  # Pydantic built-in
   ```
   - Pro: Pydantic handles validation
   - Con: Validation at API level, not domain
   - Rejected: Domain needs independent validation

**Consequences:**
- ✅ Invalid objects can't exist
- ✅ Type-safe code
- ✅ Business rules encapsulated
- ❌ More classes (Email, CPF)
- ❌ Slightly more boilerplate

**ValueObjects in This Project:**
1. **Email** — validates @ and domain format
2. **CPF** — validates mod-11 checksum, rejects all-same-digit CPFs

**CPF Validation Algorithm:**
```python
def _validar_cpf(cpf: str) -> bool:
    # Check length (11 digits)
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Check all-same-digit CPFs (always invalid)
    if len(set(cpf)) == 1:
        return False
    
    # Check first digit (mod-11)
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) != digito1:
        return False
    
    # Check second digit (mod-11)
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if int(cpf[10]) != digito2:
        return False
    
    return True
```

**Testing Strategy:**
- Unit tests validate email/CPF separately
- E2E tests ensure repository rejects invalid values

---

## ADR-005: UseCase Pattern with Request/Response Objects

**Status:** ACCEPTED ✅

**Decision:**
Each UseCase has explicit Request and Response dataclasses.

```python
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

class CriarUsuarioUseCase(UseCase):
    def executar(self, requisicao: CriarUsuarioRequest) -> CriarUsuarioResponse:
        try:
            # ... business logic ...
            return CriarUsuarioResponse(sucesso=True, usuario_id=usuario.id)
        except ValueError as e:
            return CriarUsuarioResponse(sucesso=False, mensagem=str(e))
```

**Rationale:**
- Explicit input/output contract
- Testable: create request, call UseCase, check response
- Type-safe: IDE autocomplete works
- Decouples UseCase from HTTP
- Easy to version APIs (V1Request, V2Request)

**Alternatives Considered:**

1. **Direct Method Calls**
   ```python
   def criar_usuario(nome: str, email: str, cpf: str, ...) -> dict:
   ```
   - Pro: Simpler
   - Con: Unclear what returns, no structure
   - Rejected: Not type-safe

2. **Exception-Based Errors**
   ```python
   def criar_usuario(requisicao) -> Usuario:
       if erro:
           raise UsuarioError(message)
   ```
   - Pro: Pythonic
   - Con: Hard to test, can't return structured error info
   - Rejected: Want typed responses

3. **Result Type (Success/Failure)**
   ```python
   Result[CriarUsuarioResponse, ErrorResponse]
   ```
   - Pro: Type-safe error handling
   - Con: More complex, overkill for current needs
   - Rejected: Response with sucesso flag is simpler

**Consequences:**
- ✅ Clear contracts
- ✅ Type-safe
- ✅ Easy to test
- ✅ Easy to add to HTTP layer
- ❌ More dataclasses
- ❌ Verbose per UseCase

**Response Pattern:**
```python
# Success response
response = CriarUsuarioResponse(sucesso=True, usuario_id=1)

# Error response
response = CriarUsuarioResponse(
    sucesso=False,
    mensagem="Email já existe"
)

# Always returned (never raises)
return response
```

---

## ADR-006: Pydantic v2 for Validation and Settings

**Status:** ACCEPTED ✅

**Decision:**
Use Pydantic v2 for:
- Settings management (pydantic-settings)
- Request/Response validation
- Data model validation

```python
# Settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PPP Expert IA"
    environment: str = "development"
    logs_path: Path = Path("data/logs")
    
    class Config:
        env_file = ".env"

# Validation
class CriarUsuarioRequest(BaseModel):
    nome: str  # Required
    email: str = Field(..., min_length=5)
    cpf: str = Field(..., regex=r"^\d{11}$")
```

**Rationale:**
- Industry standard for Python validation
- Excellent error messages
- Automatic documentation generation
- Type hints leverage
- Easy to convert to/from JSON

**Alternatives Considered:**

1. **Marshmallow**
   - Pro: Mature, schema-based
   - Con: More verbose, less integrated with type hints
   - Rejected: Pydantic v2 is superior

2. **No Validation**
   - Pro: Simpler code
   - Con: Invalid data propagates through system
   - Rejected: Dangerous

3. **Manual Validation**
   - Pro: Full control
   - Con: Repetitive, error-prone
   - Rejected: Reinventing wheel

**Consequences:**
- ✅ Strong typing
- ✅ Automatic validation
- ✅ Good error messages
- ✅ JSON serialization
- ❌ Dependency on Pydantic
- ❌ Slight performance overhead

---

## ADR-007: Loguru for Structured Logging

**Status:** ACCEPTED ✅

**Decision:**
Use Loguru for all logging needs.

```python
from src.core.logging import logger

logger.info("Usuário criado", extra={"usuario_id": usuario.id})
logger.debug("Validando email", extra={"email": email})
logger.error("Erro ao salvar", extra={"erro": str(e)})
```

**Rationale:**
- Better API than standard logging
- Structured logging support
- File rotation built-in
- Colorized console output
- Exception context built-in

**Alternatives Considered:**

1. **Python stdlib logging**
   - Pro: Included in Python
   - Con: Verbose setup, less intuitive
   - Rejected: Loguru is cleaner

2. **No Logging**
   - Pro: Simpler code
   - Con: Can't debug production issues
   - Rejected: Unacceptable

**Consequences:**
- ✅ Better debugging
- ✅ Production observability
- ✅ Structured logs
- ❌ External dependency
- ❌ Custom sink configuration needed

---

## Decision Log

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 001 | Five-Layer Clean Architecture | ACCEPTED | 2026-06-15 |
| 002 | Singleton Logger & Settings | ACCEPTED | 2026-06-15 |
| 003 | Repository Pattern | ACCEPTED | 2026-06-20 |
| 004 | ValueObject Pattern | ACCEPTED | 2026-06-25 |
| 005 | UseCase Request/Response | ACCEPTED | 2026-06-25 |
| 006 | Pydantic v2 Validation | ACCEPTED | 2026-06-15 |
| 007 | Loguru Structured Logging | ACCEPTED | 2026-06-15 |

---

## Review Process

When adding a new ADR:
1. Write decision with alternatives
2. Discuss with team
3. Note consequences and revisit criteria
4. Mark status (PROPOSED → ACCEPTED → SUPERSEDED)
5. Update this log

---

**Last Updated:** 2026-07-09
