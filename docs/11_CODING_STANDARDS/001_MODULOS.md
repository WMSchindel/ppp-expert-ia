# Padrão 001

# Estrutura de Módulos Python

---

## Objetivo

Definir um padrão único para criação de módulos Python no projeto
PPP Expert IA.

Todos os arquivos Python deverão seguir esta estrutura.

---

## Ordem dos elementos

1. Docstring do módulo.

2. Imports da biblioteca padrão.

3. Imports de bibliotecas externas.

4. Imports internos do projeto.

5. Constantes.

6. Classes.

7. Funções.

---

## Exemplo

```python
"""
Nome do módulo.

Descrição.

Autor:
Werner Schindel

Projeto:
PPP Expert IA
"""

from pathlib import Path

from pydantic_settings import BaseSettings

from core.version import __version__

CONSTANTE = "valor"


class MinhaClasse:
    ...


def minha_funcao():
    ...
```

---

## Imports

Os imports deverão ser separados em grupos.

Exemplo.

Biblioteca padrão

Bibliotecas externas

Módulos internos

Cada grupo será separado por uma linha em branco.

---

## Docstrings

Todo módulo deverá possuir docstring.

Toda classe deverá possuir docstring.

Toda função pública deverá possuir docstring.

---

## Comentários

Comentários devem explicar o motivo.

Nunca explicar o óbvio.

Errado.

# soma 1

x += 1

Correto.

# Ajuste exigido pela norma XYZ.

x += 1

---

## Objetivo

Todo módulo do projeto deverá apresentar a mesma organização,
facilitando manutenção, leitura e revisão de código.
