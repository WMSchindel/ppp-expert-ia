# PROJECT MASTER

> Documento Mestre do Projeto

---

# PPP Expert IA

**Produto Comercial**

Sistema Inteligente para Elaboração do Perfil Profissiográfico Previdenciário.

---

## Plataforma

**SST Platform**

---

## Framework

**SST Core**

---

# Informações Gerais

| Item           | Valor                                    |
| -------------- | ---------------------------------------- |
| Projeto        | PPP Expert IA                            |
| Plataforma     | SST Platform                             |
| Framework      | SST Core                                 |
| Linguagem      | Python 3.13                              |
| Arquitetura    | Clean Architecture                       |
| Metodologia    | Desenvolvimento Orientado por Requisitos |
| Status         | Em Desenvolvimento                       |
| Versão Atual   | 0.1.0-alpha                              |
| Data de Início | Julho/2026                               |

---

# Objetivo

Desenvolver uma plataforma inteligente para Segurança e Saúde do Trabalho capaz de interpretar documentos técnicos, consolidar informações provenientes de diversos setores da empresa, validar requisitos legais e gerar documentos oficiais.

O primeiro módulo da plataforma será o **Perfil Profissiográfico Previdenciário (PPP)**.

---

# Visão de Longo Prazo

O PPP será apenas o primeiro módulo da plataforma.

Módulos previstos:

- PPP
- LTCAT
- PGR
- Inventário de Riscos
- PCMSO
- CAT
- APR
- eSocial
- Auditorias
- Laudos Técnicos

Todos utilizarão o mesmo núcleo (**SST Core**).

---

# Arquitetura

Versão:

**Arquitetura 1.2 (Congelada)**

Princípios adotados:

- Clean Architecture
- SOLID
- Domain Driven Design
- Repository Pattern
- Service Layer
- Desenvolvimento Orientado por Requisitos
- Versionamento Semântico

---

# Estrutura Principal

```text
PPP-Expert-IA/

assets/
config/
data/
docs/
templates/
tests/

src/

README.md
PROJECT.md
PROJECT_MASTER.md
CHANGELOG.md
TODO.md
LICENSE

pyproject.toml
requirements.txt
```

---

# Organização do Código

```text
src/

main.py

initializer.py

core/

application/

domain/

infrastructure/

presentation/

shared/
```

---

# Organização do Core

```text
core/

version.py

paths.py

config/

constants/

database/

exceptions/

logging/
```

---

# Organização dos Dados

```text
data/

database/

uploads/

output/

logs/

backups/
```

---

# Estrutura da Documentação

```text
docs/

00_PROJETO/

01_SPRINTS/

02_MANUAIS/

03_TECNICO/

04_PPP/

05_REQUISITOS/
```

---

# Filosofia do Projeto

Este projeto não tem como objetivo apenas gerar PPP.

O objetivo é desenvolver uma plataforma completa de Segurança e Saúde do Trabalho, utilizando Inteligência Artificial para interpretação documental, validação técnica e geração automatizada de documentos oficiais.

Todo o sistema foi concebido para crescimento contínuo, mantendo uma arquitetura limpa, escalável e reutilizável.

---

# Princípios do Projeto

1. Código limpo.
2. Responsabilidade única.
3. Baixo acoplamento.
4. Alta coesão.
5. Testes automatizados.
6. Documentação contínua.
7. Desenvolvimento orientado por requisitos.
8. Rastreabilidade completa.
9. Versionamento semântico.
10. Evolução incremental.

---

# Fluxo Oficial de Desenvolvimento

```text
Planejamento

↓

Requisitos

↓

Projeto

↓

Implementação

↓

Testes

↓

Documentação

↓

Commit

↓

Code Review
```

---

# Roadmap

| Sprint     | Objetivo             | Status |
| ---------- | -------------------- | ------ |
| Sprint 000 | Fundação             | ✅     |
| Sprint 001 | Core Foundation      | 🔄     |
| Sprint 002 | Persistência         | ⏳     |
| Sprint 003 | Domínio              | ⏳     |
| Sprint 004 | Parsers              | ⏳     |
| Sprint 005 | Motor IA             | ⏳     |
| Sprint 006 | Motor Previdenciário | ⏳     |
| Sprint 007 | Gerador Word         | ⏳     |
| Sprint 008 | Gerador PDF          | ⏳     |
| Sprint 009 | Interface            | ⏳     |
| Sprint 010 | Versão Comercial     | ⏳     |

---

# Backlog Atual

## Sprint 001

### Core Foundation

- [ ] CF-001 - Version
- [ ] CF-002 - Paths
- [ ] CF-003 - Constants
- [ ] CF-004 - Settings
- [ ] CF-005 - Logger
- [ ] CF-006 - Initializer
- [ ] CF-007 - Application

---

# Tecnologias

| Tecnologia        | Finalidade     |
| ----------------- | -------------- |
| Python 3.13       | Linguagem      |
| VS Code           | IDE            |
| SQLite            | Banco de Dados |
| SQLAlchemy        | ORM            |
| OpenAI API        | IA             |
| python-docx       | Word           |
| docxtpl           | Templates Word |
| PyMuPDF           | PDF            |
| pdfplumber        | Extração PDF   |
| pydantic-settings | Configurações  |
| Loguru            | Logging        |

---

# Convenções

## Pastas

snake_case

## Arquivos

snake_case.py

## Classes

PascalCase

## Funções

snake_case

## Variáveis

snake_case

## Constantes

UPPER_CASE

---

# Estado Atual

## Arquitetura

✅ Congelada

## Documentação

✅ Estruturada

## Ambiente Python

✅ Configurado

## VS Code

✅ Configurado

## Metodologia

✅ Definida

## Desenvolvimento

🔄 Em andamento

---

# Próxima Entrega

Sprint 001

Pacote Core Foundation

- Version
- Paths
- Constants
- Settings
- Logger
- Initializer
- Application

---

# Objetivo da Versão 1.0

Disponibilizar um software capaz de:

- Interpretar documentos de SST.
- Consolidar informações.
- Validar inconsistências.
- Gerar PPP em Word.
- Gerar PPP em PDF.
- Produzir rastreabilidade completa.
- Preparar o sistema para expansão para outros módulos da SST.

---

# Histórico de Decisões

As decisões arquiteturais serão registradas em:

```
docs/00_PROJETO/DECISOES.md
```

---

# Documentação Principal

| Documento          | Finalidade                 |
| ------------------ | -------------------------- |
| PROJECT_MASTER.md  | Visão executiva do projeto |
| PROJECT.md         | Informações gerais         |
| CHANGELOG.md       | Histórico de versões       |
| TODO.md            | Backlog operacional        |
| GOVERNANCA.md      | Regras do projeto          |
| ARQUITETURA_1.2.md | Arquitetura oficial        |
| DECISOES.md        | Registro das decisões      |
| INDEX.md           | Índice da documentação     |

---

# Considerações Finais

Este documento representa a visão executiva do PPP Expert IA.

Toda alteração significativa de arquitetura, metodologia, escopo ou roadmap deverá refletir neste documento.

O PROJECT_MASTER.md é considerado a principal referência do projeto e deverá permanecer sincronizado com toda a documentação técnica.
