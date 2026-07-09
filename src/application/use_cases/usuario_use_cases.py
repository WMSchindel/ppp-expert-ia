"""Casos de uso para operações com Usuários."""

from dataclasses import dataclass
from typing import List
from src.application.use_cases.base_use_case import UseCase, UseCaseRequest, UseCaseResponse
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.infrastructure.persistence.repositories.usuario_repository import UsuarioRepository
from src.core.logging import logger


# ============================================================================
# REQUESTS
# ============================================================================

@dataclass
class CriarUsuarioRequest(UseCaseRequest):
    nome: str
    email: str
    cpf: str
    empresa: str
    cargo: str


@dataclass
class AtualizarCargoRequest(UseCaseRequest):
    usuario_id: int
    novo_cargo: str


@dataclass
class AtualizarEmpresaRequest(UseCaseRequest):
    usuario_id: int
    nova_empresa: str


@dataclass
class DesativarUsuarioRequest(UseCaseRequest):
    usuario_id: int


@dataclass
class ListarUsuariosAtivosRequest(UseCaseRequest):
    pass


# ============================================================================
# RESPONSES
# ============================================================================

@dataclass
class UsuarioCriadoResponse(UseCaseResponse):
    usuario_id: int = None


@dataclass
class UsuarioAtualizadoResponse(UseCaseResponse):
    usuario_id: int = None


@dataclass
class ListarUsuariosAtivosResponse(UseCaseResponse):
    usuarios: List[dict] = None


# ============================================================================
# USE CASES
# ============================================================================

class CriarUsuarioUseCase(UseCase):
    """Caso de uso para criar um novo usuário."""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def executar(self, requisicao: CriarUsuarioRequest) -> UseCaseResponse:
        """Executa a criação de um usuário."""
        try:
            # Validar e criar value objects
            email = Email(requisicao.email)
            cpf = CPF(requisicao.cpf)

            # Criar entidade
            usuario = Usuario(
                nome=requisicao.nome,
                email=email,
                cpf=cpf,
                empresa=requisicao.empresa,
                cargo=requisicao.cargo
            )

            # Persistir
            usuario_salvo = self.repository.salvar(usuario)

            return UsuarioCriadoResponse(
                sucesso=True,
                mensagem=f"Usuário {usuario_salvo.nome} criado com sucesso",
                usuario_id=usuario_salvo.id
            )
        except ValueError as e:
            logger.error(f"Erro ao criar usuário: {e}")
            return UsuarioCriadoResponse(
                sucesso=False,
                mensagem=f"Erro: {str(e)}"
            )


class AtualizarCargoUseCase(UseCase):
    """Caso de uso para atualizar cargo de um usuário."""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def executar(self, requisicao: AtualizarCargoRequest) -> UseCaseResponse:
        """Executa a atualização de cargo."""
        try:
            usuario = self.repository.buscar_por_id(requisicao.usuario_id)

            if not usuario:
                return UsuarioAtualizadoResponse(
                    sucesso=False,
                    mensagem=f"Usuário {requisicao.usuario_id} não encontrado"
                )

            usuario.atualizar_cargo(requisicao.novo_cargo)

            return UsuarioAtualizadoResponse(
                sucesso=True,
                mensagem="Cargo atualizado com sucesso",
                usuario_id=usuario.id
            )
        except ValueError as e:
            return UsuarioAtualizadoResponse(
                sucesso=False,
                mensagem=f"Erro: {str(e)}"
            )


class AtualizarEmpresaUseCase(UseCase):
    """Caso de uso para atualizar empresa de um usuário."""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def executar(self, requisicao: AtualizarEmpresaRequest) -> UseCaseResponse:
        """Executa a atualização de empresa."""
        try:
            usuario = self.repository.buscar_por_id(requisicao.usuario_id)

            if not usuario:
                return UsuarioAtualizadoResponse(
                    sucesso=False,
                    mensagem=f"Usuário {requisicao.usuario_id} não encontrado"
                )

            usuario.atualizar_empresa(requisicao.nova_empresa)

            return UsuarioAtualizadoResponse(
                sucesso=True,
                mensagem="Empresa atualizada com sucesso",
                usuario_id=usuario.id
            )
        except ValueError as e:
            return UsuarioAtualizadoResponse(
                sucesso=False,
                mensagem=f"Erro: {str(e)}"
            )


class DesativarUsuarioUseCase(UseCase):
    """Caso de uso para desativar um usuário."""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def executar(self, requisicao: DesativarUsuarioRequest) -> UseCaseResponse:
        """Executa a desativação de um usuário."""
        usuario = self.repository.buscar_por_id(requisicao.usuario_id)

        if not usuario:
            return UseCaseResponse(
                sucesso=False,
                mensagem=f"Usuário {requisicao.usuario_id} não encontrado"
            )

        usuario.desativar()

        return UseCaseResponse(
            sucesso=True,
            mensagem="Usuário desativado com sucesso"
        )


class ListarUsuariosAtivosUseCase(UseCase):
    """Caso de uso para listar usuários ativos."""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def executar(self, requisicao: ListarUsuariosAtivosRequest) -> UseCaseResponse:
        """Executa a listagem de usuários ativos."""
        usuarios = self.repository.listar_ativos()

        usuarios_dict = [
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email.valor,
                "empresa": u.empresa,
                "cargo": u.cargo
            }
            for u in usuarios
        ]

        return ListarUsuariosAtivosResponse(
            sucesso=True,
            mensagem=f"{len(usuarios)} usuários ativos encontrados",
            usuarios=usuarios_dict
        )
