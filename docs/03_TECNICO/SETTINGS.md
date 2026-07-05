---
documento: TEC-0001
titulo: Subsistema de Configuração
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 05/07/2026
status: Em Desenvolvimento
tipo: Documentação Técnica
---

# Subsistema de Configuração

## Objetivo

O subsistema de configuração é responsável por centralizar todas as
informações relacionadas à configuração da aplicação.

Seu objetivo é fornecer uma interface única para acesso às
configurações do sistema, eliminando valores duplicados e reduzindo o
acoplamento entre os módulos.

---

# Localização

```text
src/
└── core/
    └── config/
```

---

# Arquitetura

```text
core/config/

├── __init__.py
├── environments.py
├── defaults.py
└── settings.py
```

---

# Responsabilidades

O subsistema é responsável por:

- definir os ambientes de execução;
- armazenar valores padrão da aplicação;
- carregar configurações do ambiente;
- fornecer acesso centralizado às configurações.

---

# Módulos

## environments.py

### Objetivo

Define os ambientes de execução suportados pela aplicação.

### Classe

```python
Environment
```

### Valores disponíveis

| Enum        | Valor       |
| ----------- | ----------- |
| DEVELOPMENT | development |
| TEST        | test        |
| PRODUCTION  | production  |

### Motivação

A utilização de uma Enum elimina erros provocados por strings
literais espalhadas pelo código.

Exemplo incorreto:

```python
if ambiente == "dev":
```

Exemplo correto:

```python
if settings.environment == Environment.DEVELOPMENT:
```

---

## defaults.py

**Status**

⏳ Em desenvolvimento.

### Objetivo

Centralizar todos os valores padrão utilizados pela aplicação.

Exemplos:

- idioma
- codificação
- timezone
- logging
- banco de dados

---

## settings.py

**Status**

⏳ Em desenvolvimento.

### Objetivo

Carregar as configurações da aplicação a partir de:

- variáveis de ambiente;
- arquivo `.env`;
- valores padrão.

---

# Fluxo Geral

```text
                Variáveis de Ambiente
                         │
                         ▼
                  pydantic-settings
                         │
                         ▼
                   settings.py
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
    environments.py              defaults.py
           │                           │
           └─────────────┬─────────────┘
                         ▼
               Demais módulos do sistema
```

---

# Dependências

O subsistema utiliza as seguintes bibliotecas:

| Biblioteca        | Finalidade                |
| ----------------- | ------------------------- |
| enum              | Enumerações               |
| pathlib           | Manipulação de caminhos   |
| pydantic-settings | Configuração da aplicação |
| python-dotenv     | Arquivo `.env`            |

---

# Princípios Arquiteturais

O subsistema segue os seguintes princípios:

## Responsabilidade Única (SRP)

Cada módulo possui apenas uma responsabilidade.

---

## Centralização

Todas as configurações ficam concentradas em um único subsistema.

---

## Baixo Acoplamento

Os demais módulos dependem apenas da interface pública do subsistema.

---

## Segurança de Tipos

Sempre que possível são utilizados tipos específicos
(`Enum`, `Path`, etc.) em substituição a strings.

---

# Estado Atual

| Módulo          | Status |
| --------------- | :----: |
| environments.py |   ✅   |
| defaults.py     |   ⏳   |
| settings.py     |   ⏳   |

---

# Testes

Estrutura prevista:

```text
tests/

└── unit/

    └── core/

        └── config/

            ├── test_environment.py
            ├── test_defaults.py
            └── test_settings.py
```

---

# Referências

- REQ-CF-004-01 – Environment
- ADR-0002 – Estratégia de Imports
- ER-0001 – Engineering Review do módulo Environment
- PEP 8
- PEP 435
- Documentação oficial do Python
