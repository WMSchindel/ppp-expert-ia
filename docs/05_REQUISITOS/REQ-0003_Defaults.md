---
documento: REQ-CF-004-02
titulo: Especificação Técnica - Defaults
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 06/07/2026
status: Aprovado
tipo: Especificação Técnica
pacote: CF-004.02
modulo: src/core/config/defaults.py
---

# REQ-CF-004-02

# Especificação Técnica

## Módulo `defaults.py`

---

# Objetivo

Centralizar todos os valores padrão utilizados pela aplicação.

O módulo `defaults.py` é a única fonte oficial para valores padrão do
PPP Expert IA, eliminando a necessidade de constantes duplicadas ao
longo do código-fonte.

---

# Motivação

Em aplicações de médio e grande porte é comum encontrar valores
constantes repetidos em diversos módulos.

Exemplos:

- idioma padrão;
- codificação padrão;
- nível de log;
- nome do banco de dados;
- tamanho máximo de upload.

A repetição desses valores aumenta a dificuldade de manutenção e pode
introduzir inconsistências quando uma configuração precisa ser alterada.

O módulo `defaults.py` elimina esse problema centralizando todas essas
informações.

---

# Escopo

O módulo é responsável exclusivamente por definir constantes utilizadas
como valores padrão da aplicação.

Não realiza leitura de arquivos, acesso a banco de dados ou qualquer
tipo de processamento.

---

# Responsabilidades

O módulo deve:

- definir constantes globais;
- fornecer valores padrão para outros módulos;
- evitar números mágicos ("magic numbers");
- melhorar a legibilidade do código;
- facilitar futuras alterações de configuração.

---

# Não Responsabilidades

O módulo não deve:

- ler arquivos `.env`;
- acessar variáveis de ambiente;
- validar configurações;
- criar diretórios;
- executar lógica de negócio;
- instanciar objetos.

---

# Interface Pública

O módulo disponibiliza as seguintes constantes.

## Unidades de Medida

| Constante  | Tipo         | Valor           |
| ---------- | ------------ | --------------- |
| `KILOBYTE` | `Final[int]` | 1024            |
| `MEGABYTE` | `Final[int]` | 1024 × KILOBYTE |
| `GIGABYTE` | `Final[int]` | 1024 × MEGABYTE |

---

## Configuração Geral

| Constante          | Tipo         |
| ------------------ | ------------ |
| `DEFAULT_ENCODING` | `Final[str]` |
| `DEFAULT_LANGUAGE` | `Final[str]` |
| `DEFAULT_TIMEZONE` | `Final[str]` |

---

## Banco de Dados

| Constante                   | Tipo         |
| --------------------------- | ------------ |
| `DEFAULT_DATABASE_FILENAME` | `Final[str]` |

---

## Logging

| Constante               | Tipo         |
| ----------------------- | ------------ |
| `DEFAULT_LOG_LEVEL`     | `Final[str]` |
| `DEFAULT_LOG_RETENTION` | `Final[str]` |
| `DEFAULT_LOG_ROTATION`  | `Final[str]` |

---

## Upload

| Constante         | Tipo         |
| ----------------- | ------------ |
| `MAX_UPLOAD_SIZE` | `Final[int]` |

---

## Documentos

| Constante                  | Tipo         |
| -------------------------- | ------------ |
| `DEFAULT_OUTPUT_DIRECTORY` | `Final[str]` |
| `DEFAULT_WORD_TEMPLATE`    | `Final[str]` |

---

# Dependências

Bibliotecas utilizadas:

- `typing.Final`

Não existem dependências de terceiros.

---

# Fluxo de Utilização

```text
                defaults.py
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   settings.py   logger.py   demais módulos
```

---

# Critérios de Aceitação

O módulo será considerado concluído quando:

- possuir apenas constantes;
- não possuir funções;
- não possuir classes;
- utilizar `Final` em todas as constantes;
- possuir documentação do módulo;
- possuir testes unitários aprovados.

---

# Casos de Teste

| ID     | Descrição                           |
| ------ | ----------------------------------- |
| CT-001 | Validar unidades de medida          |
| CT-002 | Validar configurações gerais        |
| CT-003 | Validar configurações do banco      |
| CT-004 | Validar configurações de logging    |
| CT-005 | Validar tamanho máximo de upload    |
| CT-006 | Validar configurações de documentos |

---

# Decisões de Projeto

Durante o desenvolvimento foram adotadas as seguintes decisões:

## Uso de `Final`

Todas as constantes utilizam `typing.Final` para indicar que seus
valores não devem ser modificados durante a execução da aplicação.

---

## Eliminação de números mágicos

Ao invés de:

```python
MAX_UPLOAD_SIZE = 52428800
```

foi adotada a forma:

```python
MAX_UPLOAD_SIZE = 50 * MEGABYTE
```

Essa abordagem melhora significativamente a legibilidade do código.

---

## Organização por grupos

As constantes foram agrupadas por domínio funcional:

- unidades de medida;
- configuração geral;
- banco de dados;
- logging;
- upload;
- documentos.

Essa organização facilita a manutenção e a localização das constantes.

---

# Riscos

O principal risco é a utilização de constantes diretamente por módulos
de domínio.

As constantes deste módulo devem representar apenas configurações
globais da aplicação.

---

# Evoluções Futuras

Possíveis ampliações do módulo:

- configurações de cache;
- configurações de internacionalização;
- limites de processamento;
- configurações de exportação;
- limites de memória.

Essas ampliações deverão ocorrer somente quando houver necessidade
real, respeitando o princípio **YAGNI (You Aren't Gonna Need It)**.

---

# Referências

- REQ-CF-004-01 – Environment
- ADR-0002 – Estratégia de Imports
- PEP 8 – Style Guide for Python Code
- PEP 591 – Final qualifier
- Arquitetura do PPP Expert IA
