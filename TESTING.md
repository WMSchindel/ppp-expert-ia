# Testing Guide

Testing strategy and commands for PPP Expert IA.

---

## Test Organization

```
tests/
├─ unit/                    # Unit tests (143 tests)
│  ├─ core/                 # Logger, Settings, Config
│  ├─ domain/               # Entities, ValueObjects
│  ├─ application/          # UseCases, Services
│  ├─ infrastructure/       # Repository, Database
│  └─ presentation/         # Controllers
└─ integration/             # E2E and integration tests
```

---

## Running Tests

### Run All Tests

```bash
pytest -v
```

**Output:**
```
collected 143 items
...
============================= 143 passed in 3.67s =============================
```

### Run Specific Test File

```bash
pytest tests/unit/domain/test_usuario_entity.py -v
```

### Run Specific Test

```bash
pytest tests/unit/domain/test_usuario_entity.py::test_usuario_pode_ser_criado -v
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

Generates HTML report in `htmlcov/index.html`.

### Run by Category

```bash
# Only unit tests
pytest tests/unit/ -v

# Only integration tests
pytest tests/integration/ -v
```

### Watch Mode (Auto-rerun on changes)

```bash
pip install pytest-watch
ptw -v
```

---

## Test Coverage

Target: **90%+** coverage

### Check Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Identify Gaps

Missing lines shown with coverage report.

---

## Writing New Tests

### Unit Test Template

```python
import pytest
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF

def test_usuario_pode_ser_criado():
    """Test that usuario can be created."""
    usuario = Usuario(
        nome="Werner",
        email=Email("werner@example.com"),
        cpf=CPF("11144477735"),
        empresa="PPP",
        cargo="Dev"
    )
    
    assert usuario.nome == "Werner"
    assert usuario.ativo is True
```

### Integration Test Template

```python
@pytest.fixture
def repository():
    return UsuarioRepository()

def test_criar_e_listar(repository):
    """Test create then list flow."""
    usuario = Usuario(...)
    repository.salvar(usuario)
    
    todos = repository.listar_todos()
    assert len(todos) == 1
```

### E2E Test Template

```python
def test_e2e_criar_usuario(controller):
    """End-to-end flow: create usuario."""
    resposta = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": "11144477735",
        "empresa": "PPP",
        "cargo": "Dev"
    })
    
    assert resposta["sucesso"] is True
    assert resposta["usuario_id"] is not None
```

---

## Debugging Tests

### Run with Verbose Output

```bash
pytest -vv --tb=long
```

### Stop on First Failure

```bash
pytest -x
```

### Show Print Statements

```bash
pytest -s
```

### Drop into Debugger on Failure

```bash
pytest --pdb
```

### Show Local Variables

```bash
pytest -l
```

---

## Test Fixtures

### Database Fixture

```python
@pytest.fixture
def db_session():
    """Provide in-memory SQLite session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
```

### Controller Fixture

```python
@pytest.fixture
def controller():
    """Provide controller with in-memory repository."""
    repo = UsuarioRepository()
    return UsuarioController(repo)
```

### Helper Functions

```python
def gerar_cpf_valido(numero_base: int) -> str:
    """Generate valid CPF for testing."""
    # Implementation...
    return cpf
```

---

## CI/CD Testing

### GitHub Actions

Tests run automatically on:
- Push to main
- Pull requests
- Scheduled daily

### Local Pre-commit Hook

```bash
# .git/hooks/pre-commit
pytest -v --tb=short
```

---

## Performance Testing

### Measure Execution Time

```bash
pytest --durations=10
```

Shows 10 slowest tests.

### Target Performance

- Unit tests: < 1ms each
- Integration tests: < 100ms each
- E2E tests: < 500ms each
- Full suite: < 5 seconds

---

## Test Markers

### Mark Tests

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    ...

@pytest.mark.integration
def test_database_operation():
    ...
```

### Run by Marker

```bash
pytest -m "not slow" -v
pytest -m "integration" -v
```

---

## Common Issues

### Import Error: No module named 'src'

**Solution:** Ensure conftest.py exists in project root.

### Tests pass locally but fail in CI

**Possible causes:**
- Environment variables not set
- Database state differences
- Timing/race conditions

**Solutions:**
- Use fixtures to reset state
- Set required env vars in CI config
- Avoid time-dependent assertions

### Slow Tests

**Debug:**
```bash
pytest --durations=10
```

**Optimize:**
- Use mocks for I/O
- Cache expensive setup
- Avoid database access in unit tests

---

## Best Practices

✅ **DO:**
- Test behavior, not implementation
- Use descriptive test names
- Keep tests isolated
- Reset state between tests
- Test edge cases

❌ **DON'T:**
- Test private methods
- Create test dependencies
- Use sleep() for timing
- Mock third-party libraries
- Ignore warnings

---

## Test Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Total Tests | - | 143 |
| Coverage | 90%+ | - |
| Pass Rate | 100% | 100% ✅ |
| Avg Test Time | < 25ms | ~25ms ✅ |
| Suite Runtime | < 5s | 3.67s ✅ |

---

**Last Updated:** 2026-07-10
