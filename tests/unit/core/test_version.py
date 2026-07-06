"""
Testes do módulo version.py.
"""

from core.version import version


def test_application_name():
    """Verifica o nome oficial da aplicação."""

    assert version.app_name == "PPP Expert IA"


def test_application_version():
    """Verifica a versão atual da aplicação."""

    assert version.version == "0.1.0-alpha"


def test_application_author():
    """Verifica o autor do projeto."""

    assert version.author == "Werner"
