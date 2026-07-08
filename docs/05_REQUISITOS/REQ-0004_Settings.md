---
documento: REQ-0003
titulo: Especificação Técnica - Settings
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 07/07/2026
status: Aprovado
tipo: Especificação Técnica
pacote: CF-004.03
modulo: src/core/config/settings.py
---

# REQ-0003

# Especificação Técnica

## Módulo `settings.py`

---

# Objetivo

Implementar o componente responsável pelo carregamento e
disponibilização de todas as configurações da aplicação.

O módulo será a única interface utilizada pelos demais componentes para
acesso às configurações do sistema.

---

# Motivação

Aplicações profissionais normalmente obtêm configurações de diversas
fontes:

- arquivo `.env`;
- variáveis de ambiente;
- valores padrão.

Permitir que cada módulo realize essa leitura individualmente aumenta o
acoplamento e dificulta a manutenção.

O módulo `settings.py` centraliza esse processo.

---

# Escopo

Este módulo será responsável por:

- carregar configurações do ambiente;
- utilizar valores padrão definidos em `defaults.py`;
- disponibilizar uma interface única para acesso às configurações;
- validar automaticamente os tipos dos dados.

---

# Não Faz Parte do Escopo

O módulo não deverá:

- abrir conexões com banco de dados;
- configurar logging;
- criar diretórios;
- acessar arquivos do usuário;
- executar regras de negócio.

---

# Dependências

## Biblioteca padrão

- pathlib

## Bibliotecas externas

- pydantic-settings
- python-dotenv

## Módulos internos

- environments.py
- defaults.py

---

# Interface Pública

O módulo disponibilizará:

```python
Settings
```

e

```python
settings
```

onde:

```python
settings = Settings()
```

será a instância única utilizada por toda a aplicação.

---

# Configurações Disponíveis

## Ambiente

| Campo       | Tipo        |
| ----------- | ----------- |
| environment | Environment |

---

## Configuração Geral

| Campo    | Tipo |
| -------- | ---- |
| language | str  |
| encoding | str  |
| timezone | str  |

---

## Banco de Dados

| Campo             | Tipo |
| ----------------- | ---- |
| database_filename | str  |

---

## Logging

| Campo         | Tipo |
| ------------- | ---- |
| log_level     | str  |
| log_rotation  | str  |
| log_retention | str  |

---

## Upload

| Campo       | Tipo |
| ----------- | ---- |
| upload_size | int  |

---

## Documentos

| Campo            | Tipo |
| ---------------- | ---- |
| output_directory | str  |
| word_template    | str  |

---

# Fontes das Configurações

As configurações deverão obedecer a seguinte prioridade.

```text
Variáveis de Ambiente

        ↓

Arquivo .env

        ↓

Valores padrão (defaults.py)
```

Caso nenhuma configuração seja encontrada, será utilizado o valor
definido em `defaults.py`.

---

# Fluxo de Funcionamento

```text
                Variáveis de Ambiente
                         │
                         ▼
                   Arquivo .env
                         │
                         ▼
                pydantic-settings
                         │
                         ▼
                    Settings()
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
Environment        Defaults         Aplicação
```

---

# Critérios de Aceitação

O módulo será considerado concluído quando:

- utilizar `BaseSettings`;
- utilizar `SettingsConfigDict`;
- possuir tipagem completa;
- utilizar valores de `defaults.py`;
- utilizar `Environment`;
- possuir testes unitários;
- possuir documentação.

---

# Regras Arquiteturais

O módulo deverá obedecer às seguintes regras.

## RA-001

Nenhum módulo poderá utilizar diretamente:

```python
os.getenv(...)
```

Toda configuração deverá ser obtida através de:

```python
settings
```

---

## RA-002

Nenhum valor padrão poderá ser duplicado.

Todos deverão ser importados de:

```text
defaults.py
```

---

## RA-003

O ambiente da aplicação deverá utilizar exclusivamente a Enum
`Environment`.

---

# Casos de Teste

| ID     | Descrição                                    |
| ------ | -------------------------------------------- |
| CT-001 | Carregamento da configuração padrão          |
| CT-002 | Leitura do arquivo `.env`                    |
| CT-003 | Utilização dos valores padrão                |
| CT-004 | Validação do tipo `Environment`              |
| CT-005 | Validação dos tipos de todas as propriedades |

---

# Riscos

O principal risco é permitir que outros módulos acessem variáveis de
ambiente diretamente.

Isso quebraria a arquitetura definida para o subsistema de
configuração.

---

# Evoluções Futuras

O módulo poderá futuramente incluir:

- validação de caminhos;
- múltiplos perfis de configuração;
- configurações específicas por cliente;
- carregamento de configurações remotas.

Essas funcionalidades somente serão implementadas quando houver
necessidade real.

---

# Referências

- REQ-0001 – Environment
- REQ-0002 – Defaults
- ADR-0002 – Estratégia de Imports
- PEP 8
- Documentação do Pydantic Settings
- Arquitetura do PPP Expert IA
