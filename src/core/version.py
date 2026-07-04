"""
===============================================================================
Projeto : PPP Expert IA
Plataforma : SST Platform
Framework : SST Core

Arquivo : version.py
Módulo   : Core

Descrição:
    Centraliza as informações oficiais da aplicação.

Autor:
    Werner

Versão:
    0.1.0-alpha
===============================================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Version:
    """
    Representa os metadados oficiais da aplicação.
    """

    app_name: str = "PPP Expert IA"

    platform_name: str = "SST Platform"

    core_name: str = "SST Core"

    version: str = "0.1.0-alpha"

    author: str = "Werner"

    company: str = "PPP Expert IA"

    license: str = "MIT"

    copyright: str = "© 2026 Werner"

    description: str = (
        "Sistema Inteligente para Elaboração do "
        "Perfil Profissiográfico Previdenciário."
    )


version = Version()