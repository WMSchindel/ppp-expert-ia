---
documento: TEC-0001
titulo: Subsistema de Configuração
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.1
data: 06/07/2026
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

# Estrutura Atual

```text
core/
└── config/
    ├── __init__.py
    ├── environments.py
    ├── defaults.py
    └── settings.py
```

---

# Visão Geral da Arquitetura

```text
                    Configuração da Aplicação
                               │
      ┌────────────────────────┼────────────────────────┐
      │                        │                        │
      ▼                        ▼                        ▼
environments.py          defaults.py             settings.py
      │                        │                        │
Define os              Define valores         Carrega e fornece
ambientes              padrão                 configurações
```

---

# Responsabilidades

O subsistema é responsável por:

- definir os ambientes de execução;
- definir valores padrão da aplicação;
- carregar configurações do ambiente;
- disponibilizar configurações para os demais módulos.

---

# Módulos

---

# environments.py

## Objetivo

Representar os ambientes de execução suportados pela aplicação.

## Responsabilidade

Definir uma Enum segura para utilização em toda a aplicação.

## Interface Pública

```python
Environment
```

## Valores disponíveis

| Enum        | Valor       |
| ----------- | ----------- |
| DEVELOPMENT | development |
| TEST        | test        |
| PRODUCTION  | production  |

## Estado

✅ Implementado.

---

# defaults.py

## Objetivo

Centralizar todas as constantes padrão utilizadas pelo sistema.

Este módulo elimina números mágicos e concentra todas as configurações
estáticas da aplicação.

## Responsabilidade

Disponibilizar valores padrão para:

- configuração geral;
- logging;
- banco de dados;
- upload;
- documentos.

## Organização

```text
defaults.py

├── Unidades de Medida
├── Configuração Geral
├── Banco de Dados
├── Logging
├── Upload
└── Documentos
```

## Constantes Disponíveis

### Unidades

| Constante |
| --------- |
| KILOBYTE  |
| MEGABYTE  |
| GIGABYTE  |

---

### Configuração Geral

| Constante        |
| ---------------- |
| DEFAULT_LANGUAGE |
| DEFAULT_ENCODING |
| DEFAULT_TIMEZONE |

---

### Banco de Dados

| Constante                 |
| ------------------------- |
| DEFAULT_DATABASE_FILENAME |

---

### Logging

| Constante             |
| --------------------- |
| DEFAULT_LOG_LEVEL     |
| DEFAULT_LOG_ROTATION  |
| DEFAULT_LOG_RETENTION |

---

### Upload

| Constante       |
| --------------- |
| MAX_UPLOAD_SIZE |

---

### Documentos

| Constante                |
| ------------------------ |
| DEFAULT_OUTPUT_DIRECTORY |
| DEFAULT_WORD_TEMPLATE    |

---

## Estado

✅ Implementado.

---

# settings.py

## Objetivo

Centralizar todas as configurações carregadas pela aplicação.

## Situação Atual

⏳ Ainda não implementado.

## Responsabilidades Futuras

- carregar configurações do arquivo `.env`;
- integrar com `pydantic-settings`;
- utilizar valores de `defaults.py`;
- validar configurações;
- fornecer acesso único às configurações.

---

# Fluxo de Funcionamento

```text
                Arquivo .env
                     │
                     ▼
            pydantic-settings
                     │
                     ▼
               settings.py
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 environments.py         defaults.py
          │                     │
          └──────────┬──────────┘
                     ▼
          Demais módulos do sistema
```

---

# Dependências

| Biblioteca        | Finalidade                         |
| ----------------- | ---------------------------------- |
| enum              | Enumerações                        |
| typing            | Final                              |
| pathlib           | Manipulação de caminhos (futuro)   |
| pydantic-settings | Configuração da aplicação (futuro) |
| python-dotenv     | Leitura do arquivo `.env` (futuro) |

---

# Princípios Arquiteturais

## Responsabilidade Única

Cada módulo possui apenas uma responsabilidade claramente definida.

---

## Baixo Acoplamento

Os módulos não dependem diretamente uns dos outros.

---

## Alta Coesão

Cada módulo trata apenas de um único domínio.

---

## Código Autoexplicativo

Foram eliminados números mágicos e adotadas constantes
intermediárias sempre que possível.

Exemplo:

```python
MAX_UPLOAD_SIZE = 50 * MEGABYTE
```

---

## Segurança de Tipos

Sempre que possível são utilizados:

- Enum
- Final
- Path (futuramente)

em substituição a tipos genéricos.

---

# Testes

Estrutura atual.

```text
tests/

└── unit/

    └── core/

        └── config/

            ├── test_environment.py
            └── test_defaults.py
```

Próximo teste previsto:

```text
test_settings.py
```

---

# Estado Atual do Subsistema

| Módulo          | Status |
| --------------- | :----: |
| environments.py |   ✅   |
| defaults.py     |   ✅   |
| settings.py     |   ⏳   |

---

# Evolução Prevista

Próxima implementação:

```text
src/core/config/settings.py
```

---

# Referências

- REQ-CF-004-01 – Environment
- REQ-CF-004-02 – Defaults
- ADR-0002 – Estratégia de Imports
- ER-0001 – Environment
- ER-0002 – Defaults
- PEP 8
- PEP 435
- PEP 591
