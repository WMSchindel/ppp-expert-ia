"""SQLAlchemy ORM model for Usuario."""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UsuarioModel(Base):
    """ORM representation of Usuario entity."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    empresa = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_entity(self):
        """Convert ORM model to domain entity."""
        from src.domain.entities.usuario import Usuario
        from src.domain.value_objects.email import Email
        from src.domain.value_objects.cpf import CPF

        usuario = Usuario(
            nome=self.nome,
            email=Email(self.email),
            cpf=CPF(self.cpf),
            empresa=self.empresa,
            cargo=self.cargo,
        )
        usuario.id = self.id
        usuario.ativo = self.ativo
        usuario.data_criacao = self.data_criacao
        return usuario

    def __repr__(self):
        return f"<UsuarioModel(id={self.id}, nome={self.nome}, email={self.email})>"
