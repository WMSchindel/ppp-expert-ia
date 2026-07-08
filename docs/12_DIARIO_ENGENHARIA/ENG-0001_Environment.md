---
documento: ENG-0001
titulo: Diário de Engenharia - Environment
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 05/07/2026
status: Concluído
pacote: CF-004.01
---

# Diário de Engenharia

## Pacote

CF-004.01

---

# Objetivo da Sessão

Implementar o primeiro módulo do projeto, responsável pela definição
dos ambientes de execução da aplicação.

O objetivo secundário foi estabelecer os padrões de organização de
código, testes e documentação que serão utilizados durante todo o
desenvolvimento do PPP Expert IA.

---

# Atividades Executadas

- Implementação do módulo `environments.py`.
- Criação da Enum `Environment`.
- Implementação do primeiro teste unitário.
- Reorganização da estrutura da pasta `tests`.
- Definição da estratégia de imports.
- Criação da documentação inicial do subsistema de configuração.

---

# Problemas Encontrados

Durante a reorganização da estrutura de testes ocorreu o erro:

```text
ModuleNotFoundError: No module named 'src'
```

---

# Investigação

Foram analisados:

- Estrutura do projeto.
- Configuração do Pytest.
- Organização dos pacotes.
- Resolução de imports.
- Conteúdo do `sys.path`.

Após investigação foi constatado que o problema era causado pela
utilização de imports iniciando por `src`.

---

# Solução Adotada

Padronização dos imports utilizando apenas o pacote raiz da aplicação.

Exemplo:

```python
from core.config.environments import Environment
```

---

# Decisões Tomadas

- Estrutura definitiva da pasta `tests`.
- Estratégia de imports absolutos.
- Modelo padrão para documentação.
- Modelo padrão para Engineering Reviews.
- Modelo padrão para ADRs.
- Modelo padrão para capítulos do livro.

---

# Lições Aprendidas

- Diferença entre estrutura física e namespace lógico.
- Funcionamento básico do mecanismo de importação do Python.
- Importância da investigação antes da correção.
- Benefícios da documentação produzida em paralelo ao código.

---

# Próximo Pacote

CF-004.02

Implementação do módulo:

```text
src/core/config/defaults.py
```

---

# Observações

O módulo `Environment` passa a ser o módulo de referência para o
desenvolvimento dos próximos componentes do projeto.

Toda nova implementação deverá seguir o mesmo fluxo de engenharia
utilizado neste pacote.
