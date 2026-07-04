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
