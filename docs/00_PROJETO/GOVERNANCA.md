# Governança do Projeto

Projeto: PPP Expert IA

Nome interno: SST Platform

Versão da Arquitetura: 1.1

---

# Objetivo

Desenvolver uma plataforma inteligente para elaboração de documentos de Segurança e Saúde do Trabalho, iniciando pelo Perfil Profissiográfico Previdenciário (PPP).

---

# Princípios

- Código limpo
- SOLID
- Clean Architecture
- Domain Driven Design
- Documentação contínua
- Testes automatizados
- Desenvolvimento orientado por requisitos
- Versionamento semântico

---

# Regras

Nenhum código será desenvolvido sem requisito.

Toda Sprint deverá atualizar a documentação.

Toda funcionalidade deverá possuir teste.

Nenhum caminho poderá ser fixo no código.

Nenhum módulo poderá acessar diretamente variáveis de ambiente.

Nenhum módulo poderá acessar diretamente banco de dados sem passar pela camada de persistência.

---

# Arquitetura

Presentation

↓

Application

↓

Domain

↓

Infrastructure

↓

Core

---

# Fluxo de Desenvolvimento

Requisito

↓

Projeto

↓

Implementação

↓

Teste

↓

Documentação

↓

Commit

↓

Review

---

# Roadmap

Sprint 000

Fundação

Sprint 001

Core Foundation

Sprint 002

Persistência

Sprint 003

Domínio

Sprint 004

Parsers

Sprint 005

Motor IA

Sprint 006

Motor Previdenciário

Sprint 007

Gerador Word

Sprint 008

Gerador PDF

Sprint 009

Interface

Sprint 010

Distribuição
