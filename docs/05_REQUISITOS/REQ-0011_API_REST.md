---
documento: REQ-0011
titulo: Especificação Técnica — API REST de Usuario
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-008
---

# Especificação Técnica

## Pacote

CF-008 — Integração com API REST

---

# Objetivo

Expor casos de uso de Usuario através de endpoints REST.

---

# Endpoints

### POST /api/v1/usuarios
Criar novo usuário

**Request:**
```json
{
  "nome": "Werner",
  "email": "werner@example.com",
  "cpf": "111.444.777-35",
  "empresa": "PPP",
  "cargo": "Dev"
}
```

**Response (201):**
```json
{
  "sucesso": true,
  "mensagem": "Usuário criado",
  "usuario_id": 1
}
```

### GET /api/v1/usuarios
Listar usuários ativos

**Response (200):**
```json
{
  "sucesso": true,
  "mensagem": "2 usuários encontrados",
  "usuarios": [
    {
      "id": 1,
      "nome": "Werner",
      "email": "werner@example.com",
      "empresa": "PPP",
      "cargo": "Dev"
    }
  ]
}
```

### PUT /api/v1/usuarios/{usuario_id}/cargo
Atualizar cargo

**Request:**
```json
{
  "novo_cargo": "Senior Dev"
}
```

### PUT /api/v1/usuarios/{usuario_id}/empresa
Atualizar empresa

**Request:**
```json
{
  "nova_empresa": "Nova Empresa"
}
```

### DELETE /api/v1/usuarios/{usuario_id}
Desativar usuário

---

# Controller/Handler

**Localização:** `src/presentation/controllers/usuario_controller.py`

**Responsabilidades:**
- Receber requisições HTTP
- Validar input
- Chamar casos de uso
- Retornar respostas JSON

---

# Testes

- 8-10 testes de integração HTTP
- Validar status codes
- Validar estrutura de resposta

---

# Próxima Fase

CF-009 — Testes de Integração E2E
