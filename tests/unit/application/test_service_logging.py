"""
Testes para logging de serviços da aplicação.

Valida que serviços fazem logging correto ao serem executados.
"""

import pytest
from src.application.services import Service


class SaudacaoService(Service):
    """Serviço de exemplo para testes."""

    def executar(self, nome: str, sobrenome: str):
        """Executa o serviço de saudação."""
        return f"Olá, {nome} {sobrenome}!"


class CalculadoraService(Service):
    """Serviço que realiza operações matemáticas."""

    def executar(self, a: int, b: int, operacao: str = "soma"):
        """Executa operação matemática."""
        if operacao == "soma":
            return a + b
        elif operacao == "subtracao":
            return a - b
        elif operacao == "multiplicacao":
            return a * b
        else:
            raise ValueError(f"Operação desconhecida: {operacao}")


def test_service_can_be_created():
    """Testa que um serviço pode ser criado."""
    servico = SaudacaoService()
    assert servico is not None


def test_service_executa_method():
    """Testa que um serviço tem o método executar."""
    servico = SaudacaoService()
    resultado = servico.executar("Werner", "Schindel")
    assert resultado == "Olá, Werner Schindel!"


def test_service_can_be_called():
    """Testa que um serviço pode ser chamado como função."""
    servico = SaudacaoService()
    resultado = servico("Werner", "Schindel")
    assert resultado == "Olá, Werner Schindel!"


def test_service_with_kwargs():
    """Testa serviço com argumentos nomeados."""
    servico = CalculadoraService()
    resultado = servico(a=10, b=5, operacao="soma")
    assert resultado == 15


def test_service_with_multiple_operations():
    """Testa serviço com múltiplas operações."""
    servico = CalculadoraService()

    assert servico(a=10, b=5, operacao="soma") == 15
    assert servico(a=10, b=5, operacao="subtracao") == 5
    assert servico(a=10, b=5, operacao="multiplicacao") == 50


def test_service_error_handling():
    """Testa que serviço propaga exceções."""
    servico = CalculadoraService()

    with pytest.raises(ValueError):
        servico(a=10, b=5, operacao="operacao_invalida")
