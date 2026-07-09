---
documento: LIVRO-CF-009
titulo: Capítulo — Testes de Integração E2E
autor: Werner Schindel
data: 09/07/2026
pacote: CF-009
capitulo: 9
---

# Capítulo 9 — Testes de Integração E2E

## 9.1 Visão Geral

Após implementar todas as camadas da aplicação (Controller, UseCase, Entity, ValueObject, Repository), chegou o momento de validar que todo o sistema funciona **junto**.

Testes unitários verificam unidades isoladas. Testes E2E verificam **fluxos completos** — desde a requisição no Controller até a persistência no Repository.

### Benefícios do Teste E2E
- **Confiança:** Garante que componentes integram corretamente
- **Cobertura Real:** Testa comportamento observado pelo usuário
- **Regressão:** Detecta quando alterações quebram fluxos
- **Documentação:** Exemplifica uso correto da API

---

## 9.2 Estrutura de Teste E2E

### Padrão AAA: Arrange-Act-Assert

```python
def test_e2e_criar_e_listar(controller):
    # ARRANGE: Preparar estado inicial (controller novo, limpo)
    # (fixture @pytest.fixture fornece isso)
    
    # ACT: Executar fluxo de negócio
    resposta_criar = controller.criar_usuario({...})
    resposta_listar = controller.listar_usuarios()
    
    # ASSERT: Verificar resultado esperado
    assert resposta_listar["usuarios"][0]["nome"] == "Werner"
```

### Fixtures para Isolamento

```python
@pytest.fixture
def controller():
    repo = UsuarioRepository()  # Novo para cada teste!
    return UsuarioController(repo)
```

**Benefício:** Cada teste começa do zero → sem estado compartilhado → testes independentes.

---

## 9.3 Cenários E2E Implementados

### Cenário 1: Criar e Listar

```python
def test_e2e_criar_e_listar(controller):
    # ACT: Criar usuario
    resposta_criar = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta_criar["sucesso"]
    usuario_id = resposta_criar["usuario_id"]
    
    # ACT: Listar usuarios
    resposta_listar = controller.listar_usuarios()
    
    # ASSERT: Usuario aparece na listagem
    assert len(resposta_listar["usuarios"]) == 1
    assert resposta_listar["usuarios"][0]["id"] == usuario_id
    assert resposta_listar["usuarios"][0]["nome"] == "Werner"
```

**Fluxo Completo:**
```
Controller.criar_usuario()
  ↓
CriarUsuarioUseCase.executar()
  ↓
UsuarioRepository.salvar()
  ↓
Validação: Email/CPF únicos?
  ↓
Usuario armazenado em memória
  ↓
Controller.listar_usuarios()
  ↓
ListarUsuariosAtivosUseCase.executar()
  ↓
UsuarioRepository.listar_ativos()
  ↓
Retorna lista com usuário criado ✅
```

---

### Cenário 2: Criar → Atualizar → Verificar

```python
def test_e2e_criar_atualizar_cargo(controller):
    # Criar usuario com cargo "Dev"
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    
    # Atualizar para "Senior Dev"
    resposta = controller.atualizar_cargo(1, {"novo_cargo": "Senior Dev"})
    assert resposta["sucesso"]
    
    # Verificar que mudança persistiu
    usuarios = controller.listar_usuarios()
    assert usuarios["usuarios"][0]["cargo"] == "Senior Dev"
```

**Validação:** UseCase alterou a entidade, Repository persistiu, e leitura retorna novo valor.

---

### Cenário 3: Isolamento Entre Usuários

```python
def test_e2e_multiplos_usuarios(controller):
    # Criar usuario A
    controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    
    # Criar usuario B
    controller.criar_usuario({
        "nome": "João",
        "email": "joao@example.com",
        "cpf": gerar_cpf_valido(214741688),
        "empresa": "PPP",
        "cargo": "Analista"
    })
    
    # Listar: ambos aparecem
    resposta = controller.listar_usuarios()
    assert len(resposta["usuarios"]) == 2
    
    # Desativar A
    controller.desativar_usuario(1)
    
    # Listar: apenas B aparece
    resposta = controller.listar_usuarios()
    assert len(resposta["usuarios"]) == 1
    assert resposta["usuarios"][0]["nome"] == "João"
```

**Validação:** ListarUsuariosAtivosUseCase corretamente filtra apenas usuários ativos.

---

### Cenário 4: Validações de Duplicação

#### Email Duplicado

```python
def test_e2e_email_duplicado(controller):
    # Primeiro usuario
    resposta1 = controller.criar_usuario({
        "nome": "Werner",
        "email": "werner@example.com",
        "cpf": gerar_cpf_valido(111444777),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert resposta1["sucesso"]
    
    # Tentar criar com mesmo email
    resposta2 = controller.criar_usuario({
        "nome": "Outro",
        "email": "werner@example.com",  # DUPLICADO!
        "cpf": gerar_cpf_valido(214741688),
        "empresa": "PPP",
        "cargo": "Dev"
    })
    assert not resposta2["sucesso"]
    assert "Email" in resposta2["mensagem"]
```

**Validação:** Repository.salvar() rejeita email duplicado.

#### CPF Duplicado

```python
def test_e2e_cpf_duplicado(controller):
    cpf = gerar_cpf_valido(111444777)
    
    # Primeiro usuario
    resposta1 = controller.criar_usuario({...cpf...})
    assert resposta1["sucesso"]
    
    # Tentar criar com mesmo CPF
    resposta2 = controller.criar_usuario({...cpf...})
    assert not resposta2["sucesso"]
    assert "CPF" in resposta2["mensagem"]
```

**Validação:** Repository.salvar() rejeita CPF duplicado.

---

## 9.4 Geração Determinística de CPF

Um desafio: CPFs inválidos causariam falhas intermitentes.

### Solução: Helper gerar_cpf_valido()

```python
def gerar_cpf_valido(numero_base: int) -> str:
    """Gera CPF válido usando mod-11 checksum."""
    # Parte 1: Base + primeiro dígito verificador
    base_str = str(numero_base).zfill(9)
    soma = sum(int(base_str[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Parte 2: Base + D1 + segundo dígito verificador
    base_com_d1 = base_str + str(digito1)
    soma = sum(int(base_com_d1[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    return base_str + str(digito1) + str(digito2)
```

**Vantagens:**
- ✅ Determinístico: mesmo input → mesmo output
- ✅ Válido: passa em CPF.validar()
- ✅ Testável: no seed control, no randomness

**Exemplo:**
```python
gerar_cpf_valido(111444777)  # Sempre retorna mesmo CPF válido
gerar_cpf_valido(214741688)  # Seed diferente = CPF diferente
```

---

## 9.5 Resultados Observados

### Taxa de Sucesso
```
============================= 7 passed in 3.50s =============================

tests/integration/test_usuario_e2e.py::test_e2e_criar_e_listar PASSED    [ 14%]
tests/integration/test_usuario_e2e.py::test_e2e_criar_atualizar_cargo PASSED [ 28%]
tests/integration/test_usuario_e2e.py::test_e2e_criar_atualizar_empresa PASSED [ 42%]
tests/integration/test_usuario_e2e.py::test_e2e_criar_e_desativar PASSED [ 57%]
tests/integration/test_usuario_e2e.py::test_e2e_multiplos_usuarios PASSED [ 71%]
tests/integration/test_usuario_e2e.py::test_e2e_email_duplicado PASSED   [ 85%]
tests/integration/test_usuario_e2e.py::test_e2e_cpf_duplicado PASSED     [100%]
```

### Cobertura Total
- **129 testes passando** (122 existentes + 7 E2E)
- **0 regressões**
- **100% cenários definidos cobertos**

---

## 9.6 Padrões Aplicados

### AAA Pattern
Cada teste segue Arrange-Act-Assert:
1. **Arrange:** Fixture fornece controlador/repositório limpo
2. **Act:** Executar operações de negócio
3. **Assert:** Validar resultado esperado

### Fixture Pattern
```python
@pytest.fixture
def controller():
    return UsuarioController(UsuarioRepository())
```

Garante **isolamento**: cada teste tem seu próprio estado.

### Helper Pattern
```python
def gerar_cpf_valido(numero_base: int) -> str:
    # ... implementação
```

Evita hardcoding e garante **validade**.

---

## 9.7 Arquitetura Validada

### Stack Completo

```
┌─────────────────────────────────────┐
│   PRESENTATION LAYER                │
│   UsuarioController                 │
│   (HTTP endpoints)                  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   APPLICATION LAYER                 │
│   5 UseCases (Criar, Atualizar, ...) │
│   Request/Response objects           │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   DOMAIN LAYER                       │
│   Usuario Entity                    │
│   Email/CPF ValueObjects            │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│   INFRASTRUCTURE LAYER               │
│   UsuarioRepository                 │
│   Email/CPF uniqueness enforcement   │
└──────────────────────────────────────┘
```

**Cada camada testada E2E:**
- Controller coordena requests
- UseCase orquestra negócio
- Entity representa domínio
- Repository persiste dados
- ValueObjects validam

---

## 9.8 Lições Aprendidas

### 1. Fixture por Teste = Isolamento Total
Primeira abordagem: Usar um único controller compartilhado.
- **Problema:** Testes interferem uns com outros
- **Solução:** @pytest.fixture cria novo para cada teste

### 2. Validação no Repository
Primeira abordagem: Deixar UseCase fazer validação.
- **Problema:** Repository pode ser chamado diretamente e inserir duplicatas
- **Solução:** Validação também em Repository.salvar()

### 3. CPF Determinístico
Primeira abordagem: CPFs hardcoded (11900000000, etc)
- **Problema:** Nem todos CPFs são válidos
- **Solução:** gerar_cpf_valido() com mod-11

---

## 9.9 Próximos Passos

### CF-010: Documentação Arquitetural
- ARCH.md com diagramas
- Decision records
- Trade-offs explicados

### CF-011+: Integração com Banco Real
- SQLAlchemy ORM
- PostgreSQL
- Migrações

### CF-012+: HTTP Framework
- FastAPI ou FastAPI
- Dependency injection
- CORS, validação, etc

---

## Conclusão

Testes E2E validam que nossa **Clean Architecture** funciona corretamente. 

Cada camada faz sua parte:
- **Controller** coordena requisições
- **UseCase** orquestra negócio
- **Entity** representa domínio
- **ValueObject** valida dados
- **Repository** persiste

E quando rodamos fluxos completos (criar → listar → atualizar → desativar), tudo funciona perfeitamente.

**129 testes passando. Zero regressions. Stack validado. ✅**

