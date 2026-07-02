from src.core.version import version


def test_app_name():
    assert version.app_name == "PPP Expert IA"


def test_version():
    assert version.version == "0.1.0-alpha"


def test_author():
    assert version.author == "Werner Schindel"