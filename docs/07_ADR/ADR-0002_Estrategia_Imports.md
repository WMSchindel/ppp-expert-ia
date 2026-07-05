---
documento: ADR-0002
titulo: Estratégia de Imports do Projeto
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 05/07/2026
status: Aprovado
tipo: Architecture Decision Record
pacote: CF-004.01
---

# ADR-0002

# Estratégia de Imports do Projeto

---

# Status

✅ Aprovado

---

# Contexto

Durante a implementação do primeiro módulo (`Environment`) foi
identificado um problema relacionado à importação dos módulos da
aplicação durante a execução dos testes unitários.

Os testes utilizavam a instrução:

```python
from src.core.config.environments import Environment
```

Entretanto, essa abordagem gerou inconsistências na resolução dos
imports e não representa corretamente a arquitetura definida para o
projeto.

---

# Problema

A pasta `src` representa apenas a organização física do código-fonte.

Ela não faz parte do namespace lógico da aplicação.

Permitir imports contendo `src` criaria um forte acoplamento entre a
estrutura física do projeto e o código da aplicação.

Além disso:

- reduz a portabilidade do projeto;
- dificulta empacotamentos futuros;
- aumenta o risco de inconsistências entre ambientes de execução.

---

# Alternativas Avaliadas

## Alternativa 1

Utilizar:

```python
from src.core...
```

### Vantagens

- Simples de compreender para iniciantes.

### Desvantagens

- Acoplamento à estrutura física.
- Pouco utilizada em projetos profissionais.
- Pode causar problemas em testes e distribuição.

---

## Alternativa 2

Utilizar imports absolutos a partir do pacote raiz.

Exemplo:

```python
from core.config.environments import Environment
```

### Vantagens

- Código mais limpo.
- Independência da estrutura física.
- Compatível com a arquitetura adotada.
- Facilita manutenção.
- Facilita testes.

### Desvantagens

Nenhuma identificada para o contexto atual do projeto.

---

# Decisão

O projeto adotará exclusivamente imports absolutos iniciando no pacote
raiz da aplicação.

Exemplo:

```python
from core.config.environments import Environment
```

A utilização de imports iniciando por `src` fica oficialmente proibida.

---

# Consequências

## Positivas

- Maior clareza do código.
- Menor acoplamento.
- Facilidade para reorganização da estrutura física.
- Melhor compatibilidade com ferramentas de desenvolvimento.
- Consistência entre módulos.

## Negativas

- Pequena curva de aprendizado para desenvolvedores iniciantes.

---

# Regras Derivadas

Todos os módulos deverão seguir as seguintes regras.

## Regra 1

Utilizar apenas imports absolutos.

Correto:

```python
from core.config.settings import Settings
```

---

## Regra 2

Não utilizar:

```python
from src...
```

---

## Regra 3

Evitar imports relativos.

Evitar:

```python
from ..config import ...
```

Sempre que possível utilizar imports absolutos.

---

# Impacto

Esta decisão afeta todo o código-fonte da aplicação e deverá ser
respeitada em:

- módulos;
- testes;
- exemplos do livro;
- documentação técnica;
- futuras contribuições.

---

# Implementação

A alteração foi aplicada ao módulo:

```text
tests/unit/core/config/test_environment.py
```

que passou a utilizar:

```python
from core.config.environments import Environment
```

---

# Referências

- PEP 8
- PEP 328 – Imports
- Documentação oficial do Python
- Clean Architecture
- Arquitetura do PPP Expert IA

---

# Histórico de Revisões

| Versão | Data       | Descrição          |
| ------ | ---------- | ------------------ |
| 1.0    | 05/07/2026 | Documento inicial. |
