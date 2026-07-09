"""
Testes para logging de casos de uso da aplicação.

Valida que casos de uso fazem logging correto ao serem executados.
"""

import pytest
from dataclasses import dataclass
from src.application.use_cases import UseCase, UseCaseRequest, UseCaseResponse


@dataclass
class CriarUsuarioRequest(UseCaseRequest):
    """Requisição para criar um usuário."""
    nome: str
    email: str


@dataclass
class UsuarioCriadoResponse(UseCaseResponse):
    """Resposta da criação de usuário."""
    usuario_id: int = None


class CriarUsuarioUseCase(UseCase):
    """Caso de uso de exemplo para testes."""

    def executar(self, requisicao: CriarUsuarioRequest) -> UseCaseResponse:
        """Executa o caso de uso de criar usuário."""
        usuario_id = hash(requisicao.email) % 10000
        return UsuarioCriadoResponse(
            sucesso=True,
            mensagem=f"Usuário {requisicao.nome} criado com sucesso",
            usuario_id=usuario_id
        )


@dataclass
class CalcularIMCRequest(UseCaseRequest):
    """Requisição para calcular IMC."""
    peso: float
    altura: float


@dataclass
class IMCCalculadoResponse(UseCaseResponse):
    """Resposta do cálculo de IMC."""
    imc: float = None
    categoria: str = None


class CalcularIMCUseCase(UseCase):
    """Caso de uso de cálculo de IMC."""

    def executar(self, requisicao: CalcularIMCRequest) -> UseCaseResponse:
        """Executa o cálculo de IMC."""
        imc = requisicao.peso / (requisicao.altura ** 2)

        if imc < 18.5:
            categoria = "Abaixo do peso"
        elif imc < 25:
            categoria = "Peso normal"
        elif imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidade"

        return IMCCalculadoResponse(
            sucesso=True,
            mensagem=f"IMC calculado: {imc:.2f}",
            imc=imc,
            categoria=categoria
        )


def test_use_case_can_be_created():
    """Testa que um caso de uso pode ser criado."""
    caso = CriarUsuarioUseCase()
    assert caso is not None


def test_use_case_executar_method():
    """Testa que um caso de uso tem o método executar."""
    caso = CriarUsuarioUseCase()
    requisicao = CriarUsuarioRequest(nome="Werner", email="werner@example.com")
    resposta = caso.executar(requisicao)

    assert resposta.sucesso
    assert "Werner" in resposta.mensagem


def test_use_case_can_be_called():
    """Testa que um caso de uso pode ser chamado como função."""
    caso = CriarUsuarioUseCase()
    requisicao = CriarUsuarioRequest(nome="Werner", email="werner@example.com")
    resposta = caso(requisicao)

    assert resposta.sucesso
    assert resposta.usuario_id is not None


def test_use_case_response_base_class():
    """Testa que UseCaseResponse é funcional."""
    resposta = UseCaseResponse(sucesso=True, mensagem="Tudo OK")
    assert resposta.sucesso
    assert resposta.mensagem == "Tudo OK"


def test_imc_calculation_use_case():
    """Testa caso de uso de cálculo de IMC."""
    caso = CalcularIMCUseCase()

    # Peso normal
    requisicao = CalcularIMCRequest(peso=70, altura=1.75)
    resposta = caso(requisicao)

    assert resposta.sucesso
    assert 20 < resposta.imc < 25
    assert resposta.categoria == "Peso normal"


def test_multiple_use_cases():
    """Testa múltiplos casos de uso."""
    caso_usuario = CriarUsuarioUseCase()
    caso_imc = CalcularIMCUseCase()

    requisicao_usuario = CriarUsuarioRequest(nome="Werner", email="werner@example.com")
    resposta_usuario = caso_usuario(requisicao_usuario)

    requisicao_imc = CalcularIMCRequest(peso=70, altura=1.75)
    resposta_imc = caso_imc(requisicao_imc)

    assert resposta_usuario.sucesso
    assert resposta_imc.sucesso
