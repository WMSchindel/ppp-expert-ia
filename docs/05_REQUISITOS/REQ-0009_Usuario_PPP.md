---
documento: REQ-0009
titulo: Especificação Técnica — Entidade Usuario PPP
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-006
modulo: src/domain/entities/usuario.py
---

# Especificação Técnica

## Pacote

CF-006 — Primeira Entidade Real (Usuario PPP)

---

# Objetivo

Implementar a primeira entidade real do domínio: **Usuario PPP**.

Esta entidade representa um usuário do sistema que será responsável por 
criar e manter Perfis Profissiográficos Previdenciários.

---

# Motivação

Até agora temos infraestrutura pronta:
- ✅ Logger centralizado
- ✅ Configuração
- ✅ Classes base (Entity, Repository, etc)

Agora criamos primeira entidade real para validar que tudo funciona junto.

---

# Escopo

### Usuario (Entidade Domain)

**Atributos:**
- `id`: int (identificador único)
- `nome`: str (nome completo)
- `email`: Email (value object)
- `cpf`: CPF (value object)
- `empresa`: str (empresa onde trabalha)
- `cargo`: str (cargo/função)
- `data_criacao`: datetime (quando foi criado)
- `ativo`: bool (status do usuário)

**Métodos:**
- `__init__`: Criar novo usuário
- `desativar()`: Desativar usuário
- `atualizar_cargo(novo_cargo)`: Atualizar cargo
- `atualizar_empresa(nova_empresa)`: Atualizar empresa

### Email (Value Object)

**Atributos:**
- `endereco`: str (email válido)

**Validações:**
- Deve conter @
- Deve conter domínio
- Deve ser único (validar em repository)

### CPF (Value Object)

**Atributos:**
- `numero`: str (11 dígitos)

**Validações:**
- Deve ter 11 dígitos
- Deve ser válido (algoritmo mod 11)
- Deve ser único (validar em repository)

---

# Interface

### Criação de Usuario

```python
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF

usuario = Usuario(
    nome="Werner Schindel",
    email=Email("werner@example.com"),
    cpf=CPF("12345678901"),
    empresa="PPP Expert IA",
    cargo="Desenvolvedor"
)
```

### Repository

```python
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository

repo = UsuarioRepository(session)

# Salvar
usuario = Usuario(...)
repo.salvar(usuario)

# Buscar
usuario = repo.buscar_por_id(1)

# Listar
usuarios = repo.listar_todos()
usuarios_ativos = repo.listar_por_status(ativo=True)

# Buscar por email
usuario = repo.buscar_por_email("werner@example.com")

# Buscar por CPF
usuario = repo.buscar_por_cpf("12345678901")

# Deletar
repo.deletar(usuario)
```

---

# Requisitos de Teste

### Testes de Entidade (10 testes)

1. `test_usuario_pode_ser_criado`
2. `test_usuario_tem_id`
3. `test_usuario_tem_nome`
4. `test_usuario_tem_email_value_object`
5. `test_usuario_tem_cpf_value_object`
6. `test_usuario_criacao_com_timestamp`
7. `test_usuario_desativar`
8. `test_usuario_atualizar_cargo`
9. `test_usuario_atualizar_empresa`
10. `test_usuario_representacao_string`

### Testes de ValueObjects (6 testes)

Email (3):
- `test_email_valido`
- `test_email_invalido_sem_at`
- `test_email_igualdade`

CPF (3):
- `test_cpf_valido`
- `test_cpf_invalido_tamanho`
- `test_cpf_igualdade`

### Testes de Repository (8 testes)

1. `test_repository_salvar_usuario`
2. `test_repository_buscar_por_id`
3. `test_repository_listar_todos`
4. `test_repository_deletar`
5. `test_repository_buscar_por_email`
6. `test_repository_buscar_por_cpf`
7. `test_repository_listar_ativos`
8. `test_repository_erro_duplicado`

**Total:** 24 testes

---

# Requisitos Não-Funcionais

### Validações

- Email: deve ser válido
- CPF: deve ter 11 dígitos, passar validação mod 11
- Email único: não pode haver dois usuarios com mesmo email
- CPF único: não pode haver dois usuarios com mesmo CPF
- Nome: não vazio
- Empresa/Cargo: permitem vazio no início

### Performance

- Busca por ID: O(1)
- Busca por email: O(n) ou índice se BD
- Busca por CPF: O(n) ou índice se BD

---

# Dependências

- ✅ CF-005.03 (Entity base class)
- ✅ CF-005.04 (Repository base class)
- ✅ Logging automatizado em todas as camadas

---

# Arquitetura

```
src/domain/entities/
  └─ usuario.py (Usuario entity)

src/domain/value_objects/
  ├─ email.py (Email VO)
  └─ cpf.py (CPF VO)

src/infrastructure/persistence/repositories/
  └─ usuario_repository.py (UsuarioRepository)

tests/unit/domain/
  ├─ test_usuario.py
  ├─ test_email.py
  └─ test_cpf.py

tests/unit/infrastructure/
  └─ test_usuario_repository.py
```

---

# Critérios de Aceição

- [ ] Usuario entity implementada
- [ ] Email value object implementado
- [ ] CPF value object implementado
- [ ] UsuarioRepository implementado
- [ ] 24 testes novos, todos passando
- [ ] 99+ testes totais passando
- [ ] Sem regressões
- [ ] Logging automático em todas operações
- [ ] Documentação técnica
- [ ] Engineering review positiva

---

# Próximas Fases

CF-007 — Casos de Uso de Usuario

Objetivo: Criar use cases para:
- Criar usuario
- Atualizar usuario
- Desativar usuario
- Listar usuarios

---

# Histórico de Versões

| Versão | Data | Status | Notas |
|--------|------|--------|-------|
| 1.0 | 09/07/2026 | Rascunho | Especificação inicial |
