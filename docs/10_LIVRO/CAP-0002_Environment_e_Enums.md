---
documento: CAP-0002
titulo: Environment e Enumerações em Python
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 05/07/2026
status: Concluído
tipo: Capítulo do Livro
---

# Capítulo 2

# Environment e Enumerações em Python

---

# Objetivos

Ao final deste capítulo o leitor será capaz de:

- compreender o conceito de Enum;
- entender quando utilizar uma Enum;
- diferenciar Enum de constantes;
- compreender por que utilizamos `str` juntamente com `Enum`;
- entender a motivação arquitetural da classe `Environment`;
- interpretar o primeiro módulo desenvolvido no PPP Expert IA.

---

# Pré-requisitos

- Conhecimentos básicos de Python.
- Noções de módulos.
- Noções de classes.

---

# Motivação

Durante o desenvolvimento de um software é muito comum utilizar
strings para representar estados ou configurações.

Por exemplo:

```python
environment = "development"
```

Embora seja simples, essa abordagem apresenta diversos problemas.

Imagine um sistema com centenas de arquivos.

Em algum momento um desenvolvedor poderá escrever:

```python
environment = "Development"
```

Outro poderá utilizar:

```python
environment = "DEV"
```

Ou ainda:

```python
environment = "desenvolvimento"
```

Todas essas opções representam a mesma ideia, mas nenhuma delas é
compatível entre si.

Esse tipo de erro é extremamente difícil de identificar e pode gerar
comportamentos inesperados.

---

# A solução

Python oferece um recurso chamado **Enumeração (Enum)**.

Uma Enum representa um conjunto finito de valores permitidos.

Exemplo:

```python
from enum import Enum

class Environment(Enum):

    DEVELOPMENT = "development"

    TEST = "test"

    PRODUCTION = "production"
```

A partir desse momento, somente esses três valores passam a existir.

---

# O módulo Environment

No PPP Expert IA foi criado o módulo:

```text
src/core/config/environments.py
```

Ele possui apenas uma responsabilidade:

> Definir os ambientes de execução suportados pela aplicação.

Essa decisão segue o princípio da **Responsabilidade Única (SRP)**.

---

# Por que herdamos de str?

Observe a definição da classe:

```python
class Environment(str, Enum):
```

Ela herda de duas classes:

- `str`
- `Enum`

Isso permite que cada item da enumeração se comporte também como uma
string.

Exemplo:

```python
Environment.DEVELOPMENT.value
```

Resultado:

```text
development
```

Além disso:

```python
isinstance(Environment.DEVELOPMENT, str)
```

retorna:

```python
True
```

Essa característica facilita a integração com bibliotecas como:

- pydantic-settings
- SQLAlchemy
- FastAPI

---

# Funcionamento Interno

Quando o Python encontra:

```python
class Environment(str, Enum):
```

ele cria uma nova classe derivada de `Enum`.

Cada atributo declarado torna-se um objeto único e imutável.

Assim:

```python
Environment.DEVELOPMENT
```

não é apenas uma string.

É um objeto da classe `Environment`.

Esse objeto possui:

- nome (`DEVELOPMENT`);
- valor (`development`);
- comportamento de string.

---

# Arquitetura

```text
            settings.py
                 │
                 ▼
         Environment
                 │
        ┌────────┴────────┐
        ▼                 ▼
 DEVELOPMENT          PRODUCTION
```

O restante do sistema não trabalha com strings.

Ele trabalha com objetos do tipo `Environment`.

Isso reduz significativamente a possibilidade de erros.

---

# Testes

O primeiro teste automatizado do projeto foi criado para validar a
classe `Environment`.

Arquivo:

```text
tests/unit/core/config/test_environment.py
```

Foram verificados:

- valor DEVELOPMENT;
- valor TEST;
- valor PRODUCTION.

Todos os testes foram aprovados.

---

# Boas práticas

✔ Utilize Enum sempre que existir um conjunto finito de valores.

✔ Evite strings literais espalhadas pelo projeto.

✔ Centralize todas as enumerações.

✔ Utilize nomes claros e padronizados.

---

# Erros comuns

## Utilizar strings

Errado:

```python
if ambiente == "development":
```

Correto:

```python
if ambiente == Environment.DEVELOPMENT:
```

---

## Duplicar valores

Evite declarar os mesmos valores em vários módulos.

A Enum deve ser a única fonte da verdade.

---

# Curiosidades

A implementação de Enum foi introduzida oficialmente no Python através
da **PEP 435**, publicada em 2013.

Desde então tornou-se um recurso amplamente utilizado em aplicações
profissionais.

---

# Resumo

Neste capítulo aprendemos:

- o que é uma Enum;
- por que ela existe;
- como o Python implementa uma Enum;
- por que utilizamos `str` juntamente com `Enum`;
- como o módulo `Environment` foi projetado;
- quais vantagens arquiteturais essa abordagem oferece.

Esse foi o primeiro módulo efetivamente implementado do PPP Expert IA
e servirá como modelo para diversos componentes da plataforma.

---

# Exercícios

1. Adicione um novo ambiente chamado `STAGING`.

2. Crie um teste para validar esse novo ambiente.

3. Pesquise a diferença entre `Enum` e `StrEnum`.

4. Explique com suas palavras por que uma Enum é mais segura que uma
   string comum.

---

# Glossário

| Termo     | Definição                                                      |
| --------- | -------------------------------------------------------------- |
| Enum      | Tipo especial que representa um conjunto finito de constantes. |
| SRP       | Single Responsibility Principle.                               |
| Namespace | Espaço onde nomes são definidos e resolvidos pelo Python.      |
| PEP       | Python Enhancement Proposal.                                   |

---

# Referências

- PEP 8 – Style Guide for Python Code
- PEP 435 – Enumerations
- Documentação oficial do Python (`enum`)
- ADR-0002 – Estratégia de Imports
- REQ-CF-004-01 – Environment
- ER-0001 – Engineering Review
