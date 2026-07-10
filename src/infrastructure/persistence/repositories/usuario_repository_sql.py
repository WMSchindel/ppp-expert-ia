"""SQLAlchemy implementation of UsuarioRepository."""

from sqlalchemy.orm import Session
from src.core.logging import logger
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.infrastructure.persistence.models.usuario_model import UsuarioModel
from src.infrastructure.persistence.repositories.usuario_repository import (
    UsuarioRepository,
)


class UsuarioRepositorySQL(UsuarioRepository):
    """SQL implementation of UsuarioRepository using SQLAlchemy."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
        logger.info("UsuarioRepositorySQL initialized")

    def salvar(self, usuario: Usuario) -> None:
        """Save usuario to database."""
        logger.info("Saving usuario", extra={"email": usuario.email.valor})

        # Check email uniqueness
        if self._existe_email(usuario.email):
            logger.warning(
                "Email already exists", extra={"email": usuario.email.valor}
            )
            raise ValueError("Email já existe")

        # Check CPF uniqueness
        if self._existe_cpf(usuario.cpf):
            logger.warning("CPF already exists", extra={"cpf": usuario.cpf.valor})
            raise ValueError("CPF já existe")

        # Create model
        model = UsuarioModel(
            nome=usuario.nome,
            email=usuario.email.valor,
            cpf=usuario.cpf.valor,
            empresa=usuario.empresa,
            cargo=usuario.cargo,
            ativo=usuario.ativo,
            data_criacao=usuario.data_criacao,
        )

        # Save to database
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        # Update entity with generated ID
        usuario.id = model.id

        logger.info("Usuario saved", extra={"usuario_id": usuario.id})

    def buscar_por_id(self, id: int) -> Usuario | None:
        """Fetch usuario by ID."""
        logger.debug("Fetching usuario by ID", extra={"id": id})

        model = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).first()

        if not model:
            logger.debug("Usuario not found", extra={"id": id})
            return None

        return model.to_entity()

    def buscar_por_email(self, email: Email) -> Usuario | None:
        """Fetch usuario by email."""
        logger.debug("Fetching usuario by email", extra={"email": email.valor})

        model = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.email == email.valor)
            .first()
        )

        if not model:
            logger.debug("Usuario not found", extra={"email": email.valor})
            return None

        return model.to_entity()

    def buscar_por_cpf(self, cpf: CPF) -> Usuario | None:
        """Fetch usuario by CPF."""
        logger.debug("Fetching usuario by CPF", extra={"cpf": cpf.valor})

        model = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.cpf == cpf.valor)
            .first()
        )

        if not model:
            logger.debug("Usuario not found", extra={"cpf": cpf.valor})
            return None

        return model.to_entity()

    def listar_todos(self) -> list[Usuario]:
        """List all usuarios."""
        logger.debug("Listing all usuarios")

        models = self.db.query(UsuarioModel).all()
        usuarios = [model.to_entity() for model in models]

        logger.debug("Listed usuarios", extra={"count": len(usuarios)})
        return usuarios

    def listar_ativos(self) -> list[Usuario]:
        """List only active usuarios."""
        logger.debug("Listing active usuarios")

        models = self.db.query(UsuarioModel).filter(UsuarioModel.ativo == True).all()
        usuarios = [model.to_entity() for model in models]

        logger.debug("Listed active usuarios", extra={"count": len(usuarios)})
        return usuarios

    def deletar(self, id: int) -> None:
        """Delete usuario by ID."""
        logger.info("Deleting usuario", extra={"id": id})

        self.db.query(UsuarioModel).filter(UsuarioModel.id == id).delete()
        self.db.commit()

        logger.info("Usuario deleted", extra={"id": id})

    def contar(self) -> int:
        """Count total usuarios."""
        count = self.db.query(UsuarioModel).count()
        logger.debug("Counted usuarios", extra={"count": count})
        return count

    def _existe_email(self, email: Email) -> bool:
        """Check if email exists."""
        return (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.email == email.valor)
            .first()
            is not None
        )

    def _existe_cpf(self, cpf: CPF) -> bool:
        """Check if CPF exists."""
        return (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.cpf == cpf.valor)
            .first()
            is not None
        )
