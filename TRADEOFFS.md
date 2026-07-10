# Design Trade-offs

Understanding trade-offs behind architectural decisions.

---

## Trade-off 1: Clean Architecture vs Simplicity

### The Dilemma

**Simple Approach:**
```
single file: main.py (500 lines)
├─ Controllers
├─ Business logic
├─ Database queries
└─ Logging
```

**Clean Architecture Approach:**
```
25+ files organized in 5 layers
├─ presentation/
├─ application/
├─ domain/
├─ infrastructure/
└─ core/
```

### Analysis

| Aspect | Simple | Clean |
|--------|--------|-------|
| **Lines per file** | 500 | 50-100 |
| **Testing** | Hard | Easy |
| **Understanding** | Fast initially | Faster once learned |
| **Scaling** | Very hard | Very easy |
| **Framework changes** | Rewrite | Small changes |

### What We Chose

**✅ Clean Architecture**

### Why

1. **Project will grow** — Already planning multiple entities (Project, Task, Report, etc)
2. **Team maintainability** — New developers understand structure immediately
3. **Testing confidence** — Can test each layer independently
4. **Technology flexibility** — Can swap web framework, database, etc

### When to Revisit

If project remains single-file forever (unlikely) or becomes too complex for 5 layers.

### Cost

- Slightly more files to understand initially
- More boilerplate (dataclasses, repository interfaces)
- Longer setup time

---

## Trade-off 2: Singleton Pattern vs Dependency Injection

### The Dilemma

**Dependency Injection:**
```python
class UsuarioController:
    def __init__(self, logger: Logger, settings: Settings, repo: Repository):
        self.logger = logger
        self.settings = settings
        self.repo = repo

# Usage requires passing through entire chain
controller = UsuarioController(logger, settings, repo)
```

**Singleton:**
```python
class UsuarioController:
    def criar_usuario(self):
        logger.info("Creating...")  # Direct access
        logger.debug(f"App: {settings.app_name}")

# Usage is simple
controller = UsuarioController(repo)
```

### Analysis

| Aspect | DI | Singleton |
|--------|----|-----------| 
| **Verbosity** | Very high | Very low |
| **Testability** | Easy mock | Harder |
| **Dependencies clear?** | Yes | No |
| **Global state** | No | Yes |
| **Number of params** | 100+ | 0-2 |

### What We Chose

**✅ Singleton (Logger & Settings)**

**✅ Dependency Injection (Repository)**

### Why

Logger and Settings are:
- Used everywhere (100+ times across codebase)
- Truly global concerns (everyone needs config)
- Initialized once at startup
- Rarely need to mock/swap

Repository is:
- Domain-specific
- Needs to be swapped for testing
- Can have multiple implementations

### Hybrid Approach

```python
# Singleton (Logger, Settings)
logger.info("Event")
settings.get("LOG_LEVEL")

# Injected (Repository)
class UsuarioController:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

# In tests: inject mock repository
class MockRepository:
    def salvar(self, usuario):
        return  # Test behavior
```

### Cost

- Global state (watch for side effects)
- Harder to isolate in tests
- But pragmatic solution for global services

### When to Revisit

If logging becomes complex (multiple files, multiple levels, rotating) or settings become environment-specific.

---

## Trade-off 3: In-Memory Repository vs Real Database

### The Dilemma

**In-Memory (Current):**
```python
class UsuarioRepository:
    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}
    
    def salvar(self, usuario):
        # Data lives in memory only
        self._usuarios[usuario.id] = usuario
```

**Real Database:**
```python
class UsuarioRepositorySQL:
    def __init__(self, db_session):
        self.db = db_session
    
    def salvar(self, usuario):
        # Data persists to disk
        self.db.add(usuario)
        self.db.commit()
```

### Analysis

| Aspect | In-Memory | Database |
|--------|-----------|----------|
| **Test speed** | ~0.46s (129 tests) | ~5-10s |
| **Setup** | None | Docker/Docker-Compose |
| **Realism** | Somewhat | Very realistic |
| **Data persistence** | No | Yes |
| **Concurrent access** | No | Yes |

### What We Chose

**✅ In-Memory (for now)**

### Why

1. **Tests are fast** — 0.46s for full suite means quick feedback
2. **No dependencies** — Don't need PostgreSQL running
3. **Easy to understand** — Dictionaries are simpler than SQL
4. **Good enough for current scope** — 1 entity, basic CRUD
5. **Easy to swap** — Repository abstraction makes it trivial to add SQL

### When to Swap

**Phase transitions:**
- **Current (CF-009):** In-memory ✅
- **CF-011:** SQLAlchemy + PostgreSQL
- **CF-012+:** Add caching layer, read replicas, etc

### Cost of In-Memory

- No persistence between runs
- No concurrent access handling
- Not production-ready
- But tests don't need these

### Migration Path

```python
# Phase 1: In-memory tests (current)
repo = UsuarioRepository()  # Uses memory

# Phase 2: Database integration tests
repo = UsuarioRepositorySQL(db_session)  # Uses PostgreSQL

# Phase 3: Production
# Same interface, different implementation
# No changes needed to UseCase/Controller!
```

---

## Trade-off 4: ValueObject Validation vs UseCase Validation

### The Dilemma

**ValueObject Validation (What we do):**
```python
class Email(ValueObject):
    def __init__(self, valor: str):
        if "@" not in valor:
            raise ValueError("Invalid email")
        self._valor = valor

# Can't create invalid email
email = Email("invalid")  # Raises immediately
```

**UseCase Validation:**
```python
class CriarUsuarioUseCase:
    def executar(self, requisicao: CriarUsuarioRequest) -> Response:
        if "@" not in requisicao.email:
            return Response(sucesso=False, mensagem="Invalid email")
        
        # Email is still a string here
        usuario = Usuario(nome=..., email=requisicao.email)
```

### Analysis

| Aspect | ValueObject | UseCase |
|--------|-------------|---------|
| **Type safety** | High | Low |
| **Where validation happens** | Construction | Business logic |
| **Invalid objects possible?** | No | Yes |
| **Flexibility** | Less | More |
| **Testing** | Easier | Harder |

### What We Chose

**✅ ValueObject Validation**

### Why

1. **Domain integrity** — Business rules are in domain layer
2. **Type safety** — `Email` type means "validated"
3. **Single responsibility** — Validation in one place
4. **Can't bypass** — No way to create invalid Usuario
5. **Database guarantees** — Invalid data never in DB

### Cost

- More classes (Email, CPF)
- Slightly more boilerplate
- Must handle ValueError in UseCase

### Pattern

```python
# UseCase calls ValueObject constructor
try:
    email = Email(requisicao.email)  # Raises if invalid
    cpf = CPF(requisicao.cpf)
    usuario = Usuario(nome=..., email=email, cpf=cpf)
except ValueError as e:
    return Response(sucesso=False, mensagem=str(e))
```

---

## Trade-off 5: Eager Loading vs Lazy Initialization

### The Dilemma

**Eager Loading:**
```python
# core/logging/logger.py
from loguru import logger
logger.add(...)  # Configure immediately on import

# Used everywhere
from src.core.logging import logger
```

**Lazy Initialization:**
```python
# core/logging/logger.py
_logger = None

def get_logger():
    global _logger
    if _logger is None:
        from loguru import logger
        logger.add(...)
        _logger = logger
    return _logger

# Used everywhere
logger = get_logger()
```

### Analysis

| Aspect | Eager | Lazy |
|--------|-------|------|
| **Circular imports** | Risky | Safe |
| **First access speed** | Fast | Slow (first call) |
| **Code clarity** | Simple | Complex |
| **Startup time** | Slower | Faster |
| **Memory** | Always loaded | Only if used |

### What We Chose

**✅ Eager Loading with Careful Imports**

### Why

1. **Logger is always needed** — Every module logs something
2. **Circular imports avoided** — Don't import at top level of infrastructure modules
3. **Clear and simple** — Just import and use
4. **Startup is fine** — 0.5-1ms overhead is negligible

### Pattern Used

```python
# In modules that might cause circular imports:
from src.core.logging import logger  # At top level - OK for domain/application

# In infrastructure modules that log:
def salvar(self, usuario):
    from src.core.logging import logger  # Import in function - avoids circular import
    logger.info("Saving usuario")
```

---

## Trade-off 6: Pydantic Dataclasses vs TypedDict vs NamedTuple

### The Dilemma

**Request/Response Objects:**
```python
# Pydantic (what we use)
class CriarUsuarioRequest(BaseModel):
    nome: str
    email: str

# TypedDict
class CriarUsuarioRequest(TypedDict):
    nome: str
    email: str

# NamedTuple
class CriarUsuarioRequest(NamedTuple):
    nome: str
    email: str

# @dataclass
@dataclass
class CriarUsuarioRequest:
    nome: str
    email: str
```

### Analysis

| Aspect | Pydantic | TypedDict | NamedTuple | @dataclass |
|--------|----------|-----------|-----------|-----------|
| **Validation** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **JSON serialize** | ✅ Built-in | ❌ No | ❌ No | Manual |
| **Type checking** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Flexibility** | ✅ Fields | ❌ Limited | ❌ Fixed | ✅ Methods |
| **Immutability** | ✅ Config | ❌ No | ✅ Yes | Manual |

### What We Chose

**✅ Pydantic for API** + **✅ @dataclass for Domain**

### Why

- **API Requests:** Pydantic validates input
- **Domain Objects:** @dataclass keeps them simple
- **Response Objects:** Pydantic for serialization

### Pattern

```python
# API Validation (Pydantic)
class CriarUsuarioRequest(BaseModel):
    nome: str
    email: str
    cpf: str

# Domain Objects (@dataclass)
@dataclass
class Usuario:
    nome: str
    email: Email
    cpf: CPF

# Response Objects (Pydantic)
class CriarUsuarioResponse(BaseModel):
    sucesso: bool
    usuario_id: int | None = None
```

---

## Trade-off 7: Type Hints Everywhere vs Practical Types

### The Dilemma

**Full Type Hints:**
```python
def salvar(self, usuario: Usuario) -> None:
    """Save usuario to repository."""
    ...

def buscar_por_id(self, id: int) -> Usuario | None:
    """Fetch usuario by ID."""
    ...

def listar_todos(self) -> list[Usuario]:
    """List all usuarios."""
    ...
```

**Minimal Type Hints:**
```python
def salvar(self, usuario):
    ...

def buscar_por_id(self, id):
    ...

def listar_todos(self):
    ...
```

### Analysis

| Aspect | Full Types | Minimal |
|--------|-----------|---------|
| **IDE support** | Excellent | Poor |
| **Code clarity** | High | Low |
| **Verbosity** | High | Low |
| **Type checking** | Possible | Impossible |
| **Maintenance** | Harder (more to update) | Easier |

### What We Chose

**✅ Full Type Hints Everywhere**

### Why

1. **IDE autocomplete** — VSCode shows method signatures
2. **Early error detection** — mypy catches type errors
3. **Documentation** — Types are self-documenting
4. **Maintainability** — Clear contracts
5. **Python 3.13** — Full type hint support is modern practice

### Pattern

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    def salvar(self, objeto: T) -> None: ...
    def buscar_por_id(self, id: int) -> T | None: ...
    def listar_todos(self) -> list[T]: ...
```

---

## Summary of Trade-offs

| Trade-off | Choice | Cost | Benefit |
|-----------|--------|------|---------|
| Architecture | Clean | More files | Scalable, testable |
| Patterns | Singleton (Logger) | Global state | Simpler code |
| Database | In-Memory | Not persistent | Fast tests |
| Validation | ValueObject | More classes | Domain integrity |
| Loading | Eager | Startup time | Clear, simple |
| Types | Full | Verbosity | IDE support, safety |

---

## When to Revisit These Decisions

- **Clean Architecture:** If project stays single-domain forever (revisit annually)
- **Singleton:** If logging/config becomes complex (next year)
- **In-Memory DB:** When ready for production (CF-011)
- **ValueObject Validation:** If too restrictive (probably never)
- **Eager Loading:** If startup time becomes issue (unlikely)
- **Type Hints:** If Python adds better tooling (unlikely)

---

**Last Updated:** 2026-07-09
