# Environment

## Objetivo

O módulo `environments.py` define os ambientes de execução aceitos pela aplicação.

A utilização de uma enumeração evita o uso de strings espalhadas pelo código, reduzindo erros de digitação e centralizando os valores permitidos.

## Localização

```
src/core/config/environments.py
```

## Classe

```python
Environment
```

## Ambientes disponíveis

| Nome        | Valor       |
| ----------- | ----------- |
| DEVELOPMENT | development |
| TEST        | test        |
| PRODUCTION  | production  |

## Justificativa

Foi utilizada uma Enum derivada de `str` para permitir compatibilidade direta com bibliotecas como `pydantic-settings`, `SQLAlchemy` e `FastAPI`, mantendo a segurança de tipos.

## Testes

O módulo possui cobertura inicial através do arquivo:

```
tests/test_environment.py
```
