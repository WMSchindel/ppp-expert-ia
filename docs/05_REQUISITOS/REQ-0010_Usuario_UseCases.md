---
documento: REQ-0010
titulo: Especificação Técnica — Casos de Uso de Usuario
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-007
---

# Especificação Técnica

## Pacote

CF-007 — Casos de Uso de Usuario

---

# Objetivo

Implementar casos de uso (orquestração de negócio) para operações com usuários.

---

# Casos de Uso

### 1. Criar Usuario

**Entrada:**
- nome: str
- email: str
- cpf: str
- empresa: str
- cargo: str

**Validações:**
- Email válido (value object)
- CPF válido (value object)
- Email único
- CPF único

**Saída:**
- Usuario criado com ID

### 2. Atualizar Cargo

**Entrada:**
- usuario_id: int
- novo_cargo: str

**Validações:**
- Usuario existe
- Cargo não vazio

**Saída:**
- Usuario atualizado

### 3. Atualizar Empresa

**Entrada:**
- usuario_id: int
- nova_empresa: str

**Validações:**
- Usuario existe
- Empresa não vazia

**Saída:**
- Usuario atualizado

### 4. Desativar Usuario

**Entrada:**
- usuario_id: int

**Validações:**
- Usuario existe

**Saída:**
- Usuario desativado

### 5. Listar Usuarios Ativos

**Entrada:** (nenhuma)

**Saída:**
- Lista de usuarios ativos

---

# Testes

- 8-10 testes por caso de uso
- Total: ~50 testes novos

---

# Próxima Fase

CF-008 — Integração com API REST
