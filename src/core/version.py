"""
===============================================================================
Projeto : PPP Expert IA
Módulo  : Core
Arquivo : version.py

Descrição:
    Centraliza as informações oficiais da aplicação.
===============================================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Version:
    """Representa os metadados da aplicação."""

    app_name: str = "PPP Expert IA"
    internal_name: str = "SST Platform"
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