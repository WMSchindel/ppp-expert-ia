"""Pydantic schemas for Usuario API."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CriarUsuarioRequest(BaseModel):
    """Request to create usuario."""

    nome: str = Field(..., min_length=1, max_length=255, description="Nome do usuario")
    email: EmailStr = Field(..., description="Email do usuario")
    cpf: str = Field(..., pattern=r"^\d{11}$", description="CPF com 11 digitos")
    empresa: str = Field(..., min_length=1, max_length=255, description="Empresa")
    cargo: str = Field(..., min_length=1, max_length=255, description="Cargo")

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Werner",
                "email": "werner@example.com",
                "cpf": "11144477735",
                "empresa": "PPP",
                "cargo": "Dev",
            }
        }


class UsuarioResponse(BaseModel):
    """Response with usuario data."""

    id: int
    nome: str
    email: str
    empresa: str
    cargo: str
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True


class CriarUsuarioResponse(BaseModel):
    """Response from create usuario."""

    sucesso: bool
    mensagem: str
    usuario_id: Optional[int] = None


class ListarUsuariosResponse(BaseModel):
    """Response from list usuarios."""

    sucesso: bool
    mensagem: str
    usuarios: list = []


class AtualizarUsuarioResponse(BaseModel):
    """Response from update usuario."""

    sucesso: bool
    mensagem: str
