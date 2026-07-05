# Sprint 001 — Core Foundation

## Objetivo

Construir a infraestrutura base da aplicação.

---

## Requisitos

### CF-001

Criar o módulo Version.

### Critérios

- Nome do produto
- Nome interno
- Versão
- Autor
- Licença

---

### CF-002

Criar o módulo Paths.

Critérios

- Detectar automaticamente a raiz do projeto
- Criar diretórios inexistentes
- Centralizar todos os caminhos

---

### CF-003

Criar o módulo Settings.

Critérios

- Utilizar pydantic-settings
- Ler .env
- Validar configurações
- Não utilizar os.getenv() em outros módulos

---

CF-004

Status

🟢 Em andamento

✔ environments.py

⬜ defaults.py

⬜ settings.py

⬜ integração

⬜ documentação final

---

## Resultado esperado

Aplicação inicializando corretamente.

## Pacote CF-004.01 — Environment

| Item                  | Status |
| --------------------- | :----: |
| Especificação Técnica |   ✅   |
| Implementação         |   ✅   |
| Testes Unitários      |   ✅   |
| Engineering Review    |   ✅   |
| ADR                   |   ✅   |
| Documentação Técnica  |   ✅   |
| Capítulo do Livro     |   ✅   |
| Diário de Engenharia  |   ✅   |
| Commit                |   ⏳   |

### Entregáveis

- `core/config/environments.py`
- `tests/unit/core/config/test_environment.py`
- `REQ-CF-004-01_Environment.md`
- `ER-0001_Environment.md`
- `ADR-0002_Estrategia_Imports.md`
- `CAP-0002_Environment_e_Enums.md`
- `ENG-0001_Environment.md`
