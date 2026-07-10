"""Routes for Usuario API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.logging import logger
from src.infrastructure.persistence.database import get_db
from src.infrastructure.persistence.repositories.usuario_repository_sql import (
    UsuarioRepositorySQL,
)
from src.presentation.controllers.usuario_controller import UsuarioController
from src.presentation.schemas.usuario_schemas import (
    AtualizarUsuarioResponse,
    CriarUsuarioRequest,
    CriarUsuarioResponse,
    ListarUsuariosResponse,
)

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])


def get_repository(db: Session = Depends(get_db)) -> UsuarioRepositorySQL:
    """Dependency injection for repository."""
    return UsuarioRepositorySQL(db)


def get_controller(
    repo: UsuarioRepositorySQL = Depends(get_repository),
) -> UsuarioController:
    """Dependency injection for controller."""
    return UsuarioController(repo)


@router.post("/", status_code=201, response_model=CriarUsuarioResponse)
async def criar_usuario(
    dados: CriarUsuarioRequest,
    controller: UsuarioController = Depends(get_controller),
) -> CriarUsuarioResponse:
    """Create new usuario."""
    logger.info("POST /api/v1/usuarios", extra={"nome": dados.nome})

    resposta = controller.criar_usuario(dados.dict())

    if not resposta["sucesso"]:
        logger.warning(
            "Falha ao criar usuario", extra={"mensagem": resposta["mensagem"]}
        )
        raise HTTPException(status_code=400, detail=resposta["mensagem"])

    logger.info("Usuario criado", extra={"usuario_id": resposta["usuario_id"]})
    return CriarUsuarioResponse(
        sucesso=resposta["sucesso"],
        mensagem=resposta["mensagem"],
        usuario_id=resposta["usuario_id"],
    )


@router.get("/", status_code=200, response_model=ListarUsuariosResponse)
async def listar_usuarios(
    controller: UsuarioController = Depends(get_controller),
) -> ListarUsuariosResponse:
    """List all active usuarios."""
    logger.info("GET /api/v1/usuarios")

    resposta = controller.listar_usuarios()

    return ListarUsuariosResponse(
        sucesso=resposta["sucesso"],
        mensagem=resposta["mensagem"],
        usuarios=resposta["usuarios"],
    )


@router.put(
    "/{usuario_id}/cargo", status_code=200, response_model=AtualizarUsuarioResponse
)
async def atualizar_cargo(
    usuario_id: int,
    novo_cargo: str,
    controller: UsuarioController = Depends(get_controller),
) -> AtualizarUsuarioResponse:
    """Update usuario cargo."""
    logger.info(f"PUT /api/v1/usuarios/{usuario_id}/cargo")

    resposta = controller.atualizar_cargo(usuario_id, {"novo_cargo": novo_cargo})

    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])

    return AtualizarUsuarioResponse(
        sucesso=resposta["sucesso"], mensagem=resposta["mensagem"]
    )


@router.put(
    "/{usuario_id}/empresa", status_code=200, response_model=AtualizarUsuarioResponse
)
async def atualizar_empresa(
    usuario_id: int,
    nova_empresa: str,
    controller: UsuarioController = Depends(get_controller),
) -> AtualizarUsuarioResponse:
    """Update usuario empresa."""
    logger.info(f"PUT /api/v1/usuarios/{usuario_id}/empresa")

    resposta = controller.atualizar_empresa(usuario_id, {"nova_empresa": nova_empresa})

    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])

    return AtualizarUsuarioResponse(
        sucesso=resposta["sucesso"], mensagem=resposta["mensagem"]
    )


@router.delete(
    "/{usuario_id}", status_code=200, response_model=AtualizarUsuarioResponse
)
async def desativar_usuario(
    usuario_id: int,
    controller: UsuarioController = Depends(get_controller),
) -> AtualizarUsuarioResponse:
    """Deactivate usuario."""
    logger.info(f"DELETE /api/v1/usuarios/{usuario_id}")

    resposta = controller.desativar_usuario(usuario_id)

    if not resposta["sucesso"]:
        raise HTTPException(status_code=400, detail=resposta["mensagem"])

    return AtualizarUsuarioResponse(
        sucesso=resposta["sucesso"], mensagem=resposta["mensagem"]
    )
