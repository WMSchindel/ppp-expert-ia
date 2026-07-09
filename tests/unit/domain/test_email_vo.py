"""Testes para Email value object."""

import pytest
from src.domain.value_objects.email import Email


def test_email_valido():
    email = Email("werner@example.com")
    assert email.valor == "werner@example.com"


def test_email_normaliza_para_lowercase():
    email = Email("WERNER@EXAMPLE.COM")
    assert email.valor == "werner@example.com"


def test_email_invalido_sem_at():
    with pytest.raises(ValueError):
        Email("wernerexample.com")


def test_email_invalido_vazio():
    with pytest.raises(ValueError):
        Email("")


def test_email_igualdade():
    email1 = Email("werner@example.com")
    email2 = Email("werner@example.com")
    assert email1 == email2


def test_email_hash():
    email1 = Email("werner@example.com")
    email2 = Email("werner@example.com")
    assert hash(email1) == hash(email2)
