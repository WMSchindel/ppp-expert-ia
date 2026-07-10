# Roadmap de Desenvolvimento

Plano detalhado para continuar o desenvolvimento.

---

## Status Atual (Checkpoint)

```
✅ CONCLUÍDO:
├─ CF-009: E2E Tests (7 testes)
├─ CF-010: Architecture Documentation
├─ CF-011: SQLAlchemy Database Layer
├─ CF-012: FastAPI Framework
└─ CF-013: Technical Documentation

Status: 143 testes passando, documentação completa
```

---

## Próximos Passos (Ordenado por Prioridade)

### 🔴 FASE 1: Correções e Refinamento (1-2 dias)

#### 1.1 Corrigir Warnings do FastAPI

**O que fazer:**
- Substituir `@app.on_event()` (deprecated) por lifespan handlers
- Corrigir warnings do Pydantic v2 (usar ConfigDict)

**Comandos:**
```bash
# Editar src/main.py
# Remover @app.on_event("startup/shutdown")
# Usar lifespan context manager

# Editar src/presentation/schemas/usuario_schemas.py
# Substituir class Config por ConfigDict
```

**Tempo:** 30 min  
**Resultado:** Zero warnings

---

#### 1.2 Corrigir FastAPI Endpoint Tests

**O que fazer:**
- Recriar testes FastAPI com fixture correta
- Usar `sqlalchemy.pool.StaticPool` para SQLite

**Arquivo:** `tests/integration/test_fastapi_endpoints.py`

**Código:**
```python
@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Key fix
    )
    Base.metadata.create_all(engine)
    yield engine
```

**Tempo:** 1 hora  
**Resultado:** 10+ testes E2E passando

---

### 🟡 FASE 2: Novas Entidades (2-3 dias)

#### 2.1 Implementar Entidade "Projeto"

**O que fazer:**

1. **Criar Specification:** `REQ-0017_Projeto_Entity.md`

2. **Implementar Classe:**
   ```bash
   # src/domain/entities/projeto.py
   class Projeto(Entity):
       id: int
       nome: str
       descricao: str
       usuario_criador_id: int  # Foreign key
       data_criacao: datetime
       ativo: bool
   ```

3. **Criar ValueObjects (se necessário):**
   - Nenhum necessário inicialmente

4. **Criar Repository:**
   ```bash
   # src/infrastructure/persistence/repositories/projeto_repository.py
   class ProjetoRepository(Repository[Projeto]):
       def salvar(self, projeto: Projeto) -> None
       def buscar_por_id(self, id: int) -> Projeto
       def listar_por_usuario(self, usuario_id: int) -> list[Projeto]
   ```

5. **Criar Tests:** 20+ testes
   ```bash
   # tests/unit/infrastructure/test_projeto_repository.py
   ```

**Tempo:** 1 dia  
**Resultado:** 20+ testes novos

---

#### 2.2 Implementar Entidade "Tarefa"

**O que fazer:**

1. Criar specification
2. Implementar entity com status enum
3. Criar repository
4. Criar 20+ tests

**Status Enum:**
```python
class StatusTarefa(Enum):
    TODO = "todo"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
```

**Tempo:** 1 dia  
**Resultado:** 20+ testes novos

---

### 🟢 FASE 3: Use Cases para Novas Entidades (2 dias)

#### 3.1 Projeto Use Cases

**O que criar:**

1. `CriarProjetoUseCase`
2. `ListarProjetosPorUsuarioUseCase`
3. `AtualizarProjetoUseCase`
4. `DesativarProjetoUseCase`

**Código Base:**
```bash
# src/application/use_cases/projeto_use_cases.py
class CriarProjetoUseCase(UseCase):
    def executar(self, requisicao: CriarProjetoRequest) -> CriarProjetoResponse:
        projeto = Projeto(
            nome=requisicao.nome,
            descricao=requisicao.descricao,
            usuario_criador_id=requisicao.usuario_criador_id
        )
        self.repository.salvar(projeto)
        return CriarProjetoResponse(sucesso=True, projeto_id=projeto.id)
```

**Testes:** 10+ testes  
**Tempo:** 1 dia

---

#### 3.2 Tarefa Use Cases

**O que criar:**

1. `CriarTarefaUseCase`
2. `ListarTarefasPorProjetoUseCase`
3. `AtualizarStatusTarefaUseCase`
4. `AtribuirTarefaUseCase`

**Testes:** 10+ testes  
**Tempo:** 1 dia

---

### 🔵 FASE 4: Controllers e Endpoints (2 dias)

#### 4.1 Projeto Controller

**O que fazer:**

```bash
# src/presentation/controllers/projeto_controller.py
class ProjetoController:
    def criar_projeto(self, dados: dict) -> dict
    def listar_projetos(self, usuario_id: int) -> dict
    def atualizar_projeto(self, projeto_id: int, dados: dict) -> dict
    def desativar_projeto(self, projeto_id: int) -> dict
```

**Tempo:** 4 horas  
**Testes:** 5-7 testes

---

#### 4.2 Tarefa Controller

```bash
# src/presentation/controllers/tarefa_controller.py
class TarefaController:
    def criar_tarefa(self, dados: dict) -> dict
    def listar_tarefas(self, projeto_id: int) -> dict
    def atualizar_status(self, tarefa_id: int, novo_status: str) -> dict
    def atribuir_tarefa(self, tarefa_id: int, usuario_id: int) -> dict
```

**Tempo:** 4 horas  
**Testes:** 5-7 testes

---

#### 4.3 FastAPI Routes

**O que fazer:**

```bash
# src/presentation/routes/projetos_routes.py
router = APIRouter(prefix="/api/v1/projetos", tags=["projetos"])

@router.post("/")
async def criar_projeto(dados: CriarProjetoRequest, controller=Depends(get_controller)):
    ...

@router.get("/usuario/{usuario_id}")
async def listar_projetos(usuario_id: int, controller=Depends(get_controller)):
    ...
```

**Tempo:** 4 horas  
**Testes:** 10+ testes E2E

---

### 📚 FASE 5: Documentação (1 dia)

#### 5.1 Atualizar API.md

Adicionar novos endpoints para Projeto e Tarefa.

#### 5.2 Criar Especificações

- REQ-0017_Projeto_Entity
- REQ-0018_Tarefa_Entity
- REQ-0019_Projeto_UseCases
- REQ-0020_Tarefa_UseCases
- REQ-0021_Projeto_Tarefa_Controllers

#### 5.3 Atualizar ARCH.md

Adicionar Projeto e Tarefa ao diagrama de arquitetura.

---

## Cronograma Recomendado

```
Semana 1 (segunda a sexta):
├─ Segunda: FASE 1 (Correções) - 2 horas
├─ Terça: FASE 2.1 (Projeto Entity) - 1 dia
├─ Quarta: FASE 2.2 (Tarefa Entity) - 1 dia
├─ Quinta: FASE 3 (Use Cases) - 1 dia
└─ Sexta: FASE 4 (Controllers + Endpoints) - 1 dia

Semana 2 (segunda):
├─ Segunda: FASE 5 (Documentação) - 4 horas
└─ Testes finais + Push

Resultado esperado:
├─ +40 novas entidades/repositórios/controllers
├─ +80 novos testes
├─ Total: 223 testes
└─ 3 novas entidades integradas
```

---

## Passo a Passo Diário

### Segunda-feira (FASE 1)

```bash
# 1. Atualizar main.py (remover deprecated decorators)
nano src/main.py
# Remover @app.on_event(), usar lifespan

# 2. Atualizar schemas (Pydantic v2)
nano src/presentation/schemas/usuario_schemas.py
# Trocar Config class por ConfigDict

# 3. Testar
pytest -v
# Verificar zero warnings

# 4. Commit
git add -A
git commit -m "fix: remove deprecated FastAPI and Pydantic patterns"
git push origin main
```

---

### Terça-feira (FASE 2.1 - Projeto Entity)

```bash
# 1. Criar specification
nano docs/05_REQUISITOS/REQ-0017_Projeto_Entity.md

# 2. Criar entity
nano src/domain/entities/projeto.py

# 3. Criar repository
nano src/infrastructure/persistence/repositories/projeto_repository.py

# 4. Criar SQLAlchemy model
nano src/infrastructure/persistence/models/projeto_model.py

# 5. Criar testes
nano tests/unit/domain/test_projeto_entity.py
nano tests/unit/infrastructure/test_projeto_repository.py

# 6. Rodar testes
pytest tests/unit/domain/test_projeto_entity.py -v

# 7. Commit
git add -A
git commit -m "feat(cf-014): implement Projeto entity and repository (CF-014.01)"
git push origin main
```

---

### Quarta-feira (FASE 2.2 - Tarefa Entity)

**Mesmo padrão que terça-feira, mas para Tarefa**

---

### Quinta-feira (FASE 3 - Use Cases)

```bash
# 1. Criar use cases para Projeto
nano src/application/use_cases/projeto_use_cases.py

# 2. Criar use cases para Tarefa
nano src/application/use_cases/tarefa_use_cases.py

# 3. Criar testes
nano tests/unit/application/test_projeto_use_cases.py
nano tests/unit/application/test_tarefa_use_cases.py

# 4. Rodar todos os testes
pytest tests/unit/application/ -v

# 5. Commit
git add -A
git commit -m "feat(cf-014): implement Projeto and Tarefa use cases (CF-014.02)"
git push origin main
```

---

### Sexta-feira (FASE 4 - Controllers + Endpoints)

```bash
# 1. Criar controllers
nano src/presentation/controllers/projeto_controller.py
nano src/presentation/controllers/tarefa_controller.py

# 2. Criar routes
nano src/presentation/routes/projetos_routes.py
nano src/presentation/routes/tarefas_routes.py

# 3. Atualizar main.py para incluir novos routers
nano src/main.py
# Adicionar: app.include_router(projetos_router)
#            app.include_router(tarefas_router)

# 4. Criar testes E2E
nano tests/integration/test_projeto_endpoints.py
nano tests/integration/test_tarefa_endpoints.py

# 5. Rodar TODOS os testes
pytest -v

# 6. Commit
git add -A
git commit -m "feat(cf-014): implement Projeto/Tarefa controllers and endpoints (CF-014.03)"
git push origin main
```

---

### Segunda-feira Semana 2 (FASE 5 - Documentação)

```bash
# 1. Atualizar API.md
nano API.md
# Adicionar 8 novos endpoints (4 para Projeto, 4 para Tarefa)

# 2. Criar especificações
nano docs/05_REQUISITOS/REQ-0019_Projeto_UseCases.md
nano docs/05_REQUISITOS/REQ-0020_Tarefa_UseCases.md
nano docs/05_REQUISITOS/REQ-0021_Controllers.md

# 3. Atualizar ARCH.md
nano ARCH.md
# Adicionar Projeto e Tarefa ao diagrama

# 4. Testes finais
pytest -v --cov=src
# Verificar cobertura > 90%

# 5. Commit final
git add -A
git commit -m "docs(cf-014): complete documentation for Projeto and Tarefa entities"
git push origin main

# 6. Criar tag para release
git tag v0.2.0
git push origin v0.2.0
```

---

## Commands Rápidos para Cada Fase

### Fase 1 (Correções)
```bash
pytest -v
# Procurar por DeprecationWarning
```

### Fase 2 (Entidades)
```bash
pytest tests/unit/domain/ -v
pytest tests/unit/infrastructure/ -v
```

### Fase 3 (Use Cases)
```bash
pytest tests/unit/application/ -v
```

### Fase 4 (Controllers)
```bash
pytest tests/integration/ -v
```

### Fase 5 (Documentação)
```bash
pytest -v --cov=src --cov-report=html
# Abrir htmlcov/index.html para verificar cobertura
```

---

## Checklist Final (Antes de Commitar)

- [ ] Todos os testes passam (`pytest -v`)
- [ ] Sem warnings (`grep -i warning`)
- [ ] Tipo hints em todas as funções
- [ ] Docstrings nas classes públicas
- [ ] Testes novos adicionados
- [ ] Cobertura > 90%
- [ ] API.md atualizado
- [ ] Commit com mensagem clara

---

## Próximas Fases (Após CF-014)

```
CF-015: Authentication & Authorization (JWT)
CF-016: Validação de Relacionamentos (FK constraints)
CF-017: Testes de Performance & Carga
CF-018: Implementação de Cache (Redis)
CF-019: Deployment em Kubernetes
CF-020: CI/CD Pipeline Completo
```

---

**Pronto para começar? Execute o passo a passo acima! 🚀**
