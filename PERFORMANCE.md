# Performance Guide

Performance optimization strategies.

---

## Current Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Test Suite | 3.67s | < 5s |
| Avg Test | ~25ms | < 30ms |
| API Response | < 50ms | < 100ms |
| Database Query | < 10ms | < 20ms |

---

## Database Optimization

### Query Performance

**Identify slow queries:**
```bash
# Enable SQL logging
echo "echo=true" >> .env.local

# Run tests and check logs
pytest -s
```

### Indexing Strategy

Current indexes:
```python
# In UsuarioModel
email = Column(String, index=True)  # Quick email lookup
cpf = Column(String, index=True)    # Quick CPF lookup
```

**Add index for frequent queries:**
```python
ativo = Column(Boolean, index=True)  # For listar_ativos()
```

### Connection Pooling

SQLAlchemy pooling already optimized:
```python
pool_size=20              # Keep 20 connections ready
max_overflow=40           # Allow 40 additional connections
```

### N+1 Query Prevention

**Bad:**
```python
usuarios = repo.listar_todos()
for usuario in usuarios:
    print(usuario.email.valor)  # Database call per user
```

**Good:**
```python
usuarios = repo.listar_todos()  # Single query
for usuario in usuarios:
    print(usuario.email.valor)  # No additional queries
```

---

## API Response Optimization

### Caching Strategy

**Cache lista de usuarios (read-heavy):**
```python
from functools import lru_cache

@lru_cache(maxsize=1)
def listar_usuarios_cached():
    return repository.listar_usuarios()

# Clear cache on update
def criar_usuario(...):
    listar_usuarios_cached.cache_clear()
```

### Response Size

**Current:** ~500 bytes per usuario  
**Target:** < 1KB

Keep response minimal:
- Only return necessary fields
- Use pagination (limit/offset)

---

## Code Performance

### Function Profiling

Identify slow functions:
```bash
pip install py-spy

py-spy record -o profile.svg -- uvicorn src.main:app
```

### Optimize Hot Paths

**Hot path:** CPF validation (called on every create)

```python
# ❌ SLOW: Recalculates every time
def validar_cpf(cpf: str) -> bool:
    # Complex validation logic
    
# ✅ FAST: Cache validation regex
import re
CPF_PATTERN = re.compile(r'^\d{11}$')
def validar_cpf(cpf: str) -> bool:
    return bool(CPF_PATTERN.match(cpf))
```

---

## Testing Performance

### Test Suite Speed

Current: 3.67s for 143 tests  
Per test: ~25ms average

**Breakdown:**
- Unit tests: ~120 tests, 2s total
- Integration tests: ~23 tests, 1.67s total

**Keep tests fast:**
- Use mocks for I/O
- Avoid database in unit tests
- Use in-memory SQLite

### Parallel Testing

```bash
pip install pytest-xdist

pytest -n 4  # Run on 4 CPU cores
```

Expected speedup: ~3x

---

## Async Operations

Future optimization (CF-015+):

```python
# Current: Synchronous
def criar_usuario(self, dados):
    usuario = Usuario(...)
    self.repository.salvar(usuario)
    return usuario

# Future: Asynchronous
async def criar_usuario_async(self, dados):
    usuario = Usuario(...)
    await self.repository.salvar_async(usuario)
    return usuario
```

---

## Monitoring

### Application Metrics

Track in production:
- Request latency (p50, p95, p99)
- Error rate
- Active requests
- Database query time

### Tools

```bash
# Development
pip install prometheus-client

# Production
pip install datadog
```

---

## Load Testing

### Test with Locust

```bash
pip install locust

# locustfile.py
from locust import HttpUser, task

class APIUser(HttpUser):
    @task
    def criar_usuario(self):
        self.client.post("/api/v1/usuarios", json={...})
    
    @task
    def listar_usuarios(self):
        self.client.get("/api/v1/usuarios")
```

Run:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

### Target Load

- 1000 concurrent users
- < 100ms p95 latency
- < 1% error rate

---

## Database Connection Pooling

### Current Configuration

```python
pool_size=20
max_overflow=40
pool_pre_ping=True        # Verify connections alive
pool_recycle=3600         # Recycle after 1 hour
```

### Tuning for Production

Scale based on concurrent users:

```
Users: 10-50    → pool_size=5, max_overflow=10
Users: 50-100   → pool_size=10, max_overflow=20
Users: 100-500  → pool_size=20, max_overflow=40
Users: 500+     → pool_size=50, max_overflow=100
```

---

## Memory Optimization

### Current Usage

```
Base: ~50MB
Per request: ~5MB
Peak: ~200MB
```

### Reduce Memory

- Use generators for large lists
- Clear caches regularly
- Avoid loading entire tables

---

## Caching Strategy

### HTTP Caching

```python
@app.get("/api/v1/usuarios", 
         headers={"Cache-Control": "max-age=60"})
async def listar_usuarios():
    # Cache GET requests for 60 seconds
    ...
```

### Redis Caching (Future)

```python
from redis import Redis

redis = Redis(host='localhost')
redis.setex('usuarios:list', 60, json.dumps(usuarios))
```

---

## Performance Benchmarks

### Target Benchmarks

| Operation | Current | Target |
|-----------|---------|--------|
| Create Usuario | ~5ms | < 10ms |
| List Usuarios | ~3ms | < 5ms |
| Update Cargo | ~4ms | < 8ms |
| Test Suite | 3.67s | < 5s |

### Measure

```bash
# Benchmark specific operation
pytest tests/unit/infrastructure/test_usuario_repository.py -v --durations=5
```

---

## Deployment Performance

### Asset Optimization

When adding static files:
- Minify CSS/JS
- Optimize images (WebP)
- Use CDN

### Database Tuning

Production PostgreSQL:

```sql
-- Add indexes
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_cpf ON usuarios(cpf);
CREATE INDEX idx_usuarios_ativo ON usuarios(ativo);

-- Analyze for optimization
ANALYZE usuarios;
```

---

**Last Updated:** 2026-07-10
