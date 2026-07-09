"""Controller para endpoints de Usuario."""

from dataclasses import asdict
from src.application.use_cases.usuario_use_cases import (
    CriarUsuarioUseCase, CriarUsuarioRequest,
    AtualizarCargoUseCase, AtualizarCargoRequest,
    AtualizarEmpresaUseCase, AtualizarEmpresaRequest,
    DesativarUsuarioUseCase, DesativarUsuarioRequest,
    ListarUsuariosAtivosUseCase, ListarUsuariosAtivosRequest
)
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository
from src.core.logging import logger


class UsuarioController:
    """Controller que coordena requisições de Usuario."""

    def __init__(self, repository: UsuarioRepository):
        """Inicializa o controller com repositório."""
        self.repository = repository
        self.criar_caso = CriarUsuarioUseCase(repository)
        self.atualizar_cargo_caso = AtualizarCargoUseCase(repository)
        self.atualizar_empresa_caso = AtualizarEmpresaUseCase(repository)
        self.desativar_caso = DesativarUsuarioUseCase(repository)
        self.listar_caso = ListarUsuariosAtivosUseCase(repository)
        logger.info("UsuarioController inicializado")

    def criar_usuario(self, dados: dict) -> dict:
        """POST /api/v1/usuarios

        Args:
            dados: {nome, email, cpf, empresa, cargo}

        Returns:
            Response dict com sucesso e usuario_id
        """
        logger.info("POST /api/v1/usuarios")
        logger.debug(f"Dados recebidos: {list(dados.keys())}")

        requisicao = CriarUsuarioRequest(**dados)
        resposta = self.criar_caso(requisicao)

        return {
            "sucesso": resposta.sucesso,
            "mensagem": resposta.mensagem,
            "usuario_id": resposta.usuario_id
        }

    def listar_usuarios(self) -> dict:
        """GET /api/v1/usuarios

        Returns:
            Response dict com lista de usuarios
        """
        logger.info("GET /api/v1/usuarios")

        requisicao = ListarUsuariosAtivosRequest()
        resposta = self.listar_caso(requisicao)

        return {
            "sucesso": resposta.sucesso,
            "mensagem": resposta.mensagem,
            "usuarios": resposta.usuarios or []
        }

    def atualizar_cargo(self, usuario_id: int, dados: dict) -> dict:
        """PUT /api/v1/usuarios/{usuario_id}/cargo

        Args:
            usuario_id: ID do usuário
            dados: {novo_cargo}

        Returns:
            Response dict com sucesso
        """
        logger.info(f"PUT /api/v1/usuarios/{usuario_id}/cargo")

        requisicao = AtualizarCargoRequest(
            usuario_id=usuario_id,
            novo_cargo=dados.get("novo_cargo")
        )
        resposta = self.atualizar_cargo_caso(requisicao)

        return {
            "sucesso": resposta.sucesso,
            "mensagem": resposta.mensagem
        }

    def atualizar_empresa(self, usuario_id: int, dados: dict) -> dict:
        """PUT /api/v1/usuarios/{usuario_id}/empresa

        Args:
            usuario_id: ID do usuário
            dados: {nova_empresa}

        Returns:
            Response dict com sucesso
        """
        logger.info(f"PUT /api/v1/usuarios/{usuario_id}/empresa")

        requisicao = AtualizarEmpresaRequest(
            usuario_id=usuario_id,
            nova_empresa=dados.get("nova_empresa")
        )
        resposta = self.atualizar_empresa_caso(requisicao)

        return {
            "sucesso": resposta.sucesso,
            "mensagem": resposta.mensagem
        }

    def desativar_usuario(self, usuario_id: int) -> dict:
        """DELETE /api/v1/usuarios/{usuario_id}

        Args:
            usuario_id: ID do usuário

        Returns:
            Response dict com sucesso
        """
        logger.info(f"DELETE /api/v1/usuarios/{usuario_id}")

        requisicao = DesativarUsuarioRequest(usuario_id=usuario_id)
        resposta = self.desativar_caso(requisicao)

        return {
            "sucesso": resposta.sucesso,
            "mensagem": resposta.mensagem
        }
