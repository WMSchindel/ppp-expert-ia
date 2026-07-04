"""
Módulo: environments.py

Define os ambientes de execução suportados pelo PPP Expert IA.

Este módulo centraliza a definição dos ambientes utilizados pela
aplicação, evitando o uso de strings espalhadas pelo código.

Autor:
Werner Schindel

Projeto:
PPP Expert IA
"""

from enum import Enum


class Environment(str, Enum):
    """
    Representa os ambientes de execução da aplicação.

    A herança de ``str`` permite que os valores da enumeração sejam
    utilizados diretamente como strings quando necessário.

    Attributes
    ----------
    DEVELOPMENT
        Ambiente de desenvolvimento.

    TEST
        Ambiente de testes.

    PRODUCTION
        Ambiente de produção.
    """

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"