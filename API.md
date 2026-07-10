# API Reference

PPP Expert IA — REST API Documentation

---

## Base URL

```
Development: http://localhost:8000
Production: https://api.ppp-expert-ia.com
```

---

## Authentication

Currently no authentication required. (To be implemented in CF-014+)

---

## Common Response Format

All responses follow this format:

```json
{
  "sucesso": true,
  "mensagem": "Operation completed",
  "data": {}
}
```

---

## Endpoints

### 1. POST /api/v1/usuarios

Create new usuario.

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Werner",
    "email": "werner@example.com",
    "cpf": "11144477735",
    "empresa": "PPP",
    "cargo": "Dev"
  }'
```

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| nome | string | ✅ | User name (1-255 chars) |
| email | string | ✅ | Email (must be valid) |
| cpf | string | ✅ | CPF (11 digits) |
| empresa | string | ✅ | Company name |
| cargo | string | ✅ | Job title |

**Response (201):**

```json
{
  "sucesso": true,
  "mensagem": "Usuario criado",
  "usuario_id": 1
}
```

**Errors:**

| Code | Error | Description |
|------|-------|-------------|
| 400 | Email já existe | Email must be unique |
| 400 | CPF já existe | CPF must be unique |
| 422 | Validation error | Invalid input format |

---

### 2. GET /api/v1/usuarios

List all active usuarios.

**Request:**

```bash
curl -X GET http://localhost:8000/api/v1/usuarios
```

**Response (200):**

```json
{
  "sucesso": true,
  "mensagem": "2 usuarios encontrados",
  "usuarios": [
    {
      "id": 1,
      "nome": "Werner",
      "email": "werner@example.com",
      "empresa": "PPP",
      "cargo": "Dev",
      "ativo": true,
      "data_criacao": "2026-07-10T10:00:00"
    }
  ]
}
```

**Query Parameters:**

None currently. (Pagination planned for CF-014+)

---

### 3. PUT /api/v1/usuarios/{usuario_id}/cargo

Update usuario cargo.

**Request:**

```bash
curl -X PUT http://localhost:8000/api/v1/usuarios/1/cargo?novo_cargo=Senior%20Dev
```

**Parameters:**

- `usuario_id` (path): Usuario ID
- `novo_cargo` (query): New cargo value

**Response (200):**

```json
{
  "sucesso": true,
  "mensagem": "Cargo atualizado"
}
```

**Errors:**

| Code | Error |
|------|-------|
| 400 | Usuario não encontrado |
| 422 | Validation error |

---

### 4. PUT /api/v1/usuarios/{usuario_id}/empresa

Update usuario empresa.

**Request:**

```bash
curl -X PUT http://localhost:8000/api/v1/usuarios/1/empresa?nova_empresa=Nova%20Empresa
```

**Parameters:**

- `usuario_id` (path): Usuario ID
- `nova_empresa` (query): New empresa value

**Response (200):**

```json
{
  "sucesso": true,
  "mensagem": "Empresa atualizada"
}
```

---

### 5. DELETE /api/v1/usuarios/{usuario_id}

Deactivate usuario (soft delete).

**Request:**

```bash
curl -X DELETE http://localhost:8000/api/v1/usuarios/1
```

**Parameters:**

- `usuario_id` (path): Usuario ID

**Response (200):**

```json
{
  "sucesso": true,
  "mensagem": "Usuario desativado"
}
```

Note: User is deactivated, not deleted. They won't appear in listings.

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized (future) |
| 403 | Forbidden (future) |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## OpenAPI Documentation

Interactive API docs available at:

```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
OpenAPI JSON: http://localhost:8000/openapi.json
```

---

## Rate Limiting

Currently unlimited. (To be implemented in CF-014+)

---

## Versioning

API version is `v1`. Future versions will use `/api/v2/`.

---

## Examples

### Create User Flow

```bash
# 1. Create usuario
curl -X POST http://localhost:8000/api/v1/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria",
    "email": "maria@example.com",
    "cpf": "22244488856",
    "empresa": "TechCorp",
    "cargo": "Analista"
  }'

# Response:
# {"sucesso": true, "mensagem": "Usuario criado", "usuario_id": 2}

# 2. List usuarios
curl -X GET http://localhost:8000/api/v1/usuarios

# 3. Update cargo
curl -X PUT http://localhost:8000/api/v1/usuarios/2/cargo?novo_cargo=Senior%20Analista

# 4. Deactivate
curl -X DELETE http://localhost:8000/api/v1/usuarios/2
```

---

**Last Updated:** 2026-07-10
