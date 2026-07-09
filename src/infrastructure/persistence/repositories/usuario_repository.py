"""
Repositório para persistência de Usuários.

Implementa a abstração de persistência para entidades Usuario,
fornecendo operações CRUD e buscas especializadas.
"""

from typing import List, Optional
from src.infrastructure.persistence.base_repository import Repository
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.core.logging import logger


class UsuarioRepository(Repository[Usuario]):
    """Repositório para persistência de usuários.

    Implementa operações CRUD e buscas especializadas para Usuario.
    """

    def __init__(self, session=None):
        """Inicializa o repositório de usuários."""
        super().__init__(session)
        self.usuarios: dict[int, Usuario] = {}
        self.proximo_id = 1

    def salvar(self, usuario: Usuario) -> Usuario:
        """Salva um usuário.

        Args:
            usuario: Usuario a salvar

        Returns:
            Usuario salvo

        Raises:
            ValueError: Se email ou CPF duplicado
        """
        self._log_operacao("Salvando", "Usuario")

        # Validar email único
        email_str = usuario.email.valor
        if any(u.email.valor == email_str for u in self.usuarios.values()):
            self._log_erro("Salvar", "Usuario", ValueError("Email já existe"))
            raise ValueError(f"Email {email_str} já existe")

        # Validar CPF único
        cpf_str = usuario.cpf.valor
        if any(u.cpf.valor == cpf_str for u in self.usuarios.values()):
            self._log_erro("Salvar", "Usuario", ValueError("CPF já existe"))
            raise ValueError(f"CPF {cpf_str} já existe")

        # Atribuir ID se novo
        if usuario.id is None:
            usuario.id = self.proximo_id
            self.proximo_id += 1

        self.usuarios[usuario.id] = usuario
        logger.debug(f"Usuario salvo com ID {usuario.id}")
        return usuario

    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        """Busca um usuário por ID.

        Args:
            id: ID do usuário

        Returns:
            Usuario se encontrado, None caso contrário
        """
        self._log_operacao("Buscando", f"Usuario #{id}")
        return self.usuarios.get(id)

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca um usuário por email.

        Args:
            email: Email do usuário

        Returns:
            Usuario se encontrado, None caso contrário
        """
        logger.info(f"Buscando Usuario por email: {email}")
        for usuario in self.usuarios.values():
            if usuario.email.valor == email.lower():
                logger.debug(f"Usuario encontrado: {usuario.id}")
                return usuario
        logger.debug("Usuario não encontrado")
        return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Usuario]:
        """Busca um usuário por CPF.

        Args:
            cpf: CPF do usuário

        Returns:
            Usuario se encontrado, None caso contrário
        """
        logger.info(f"Buscando Usuario por CPF")
        for usuario in self.usuarios.values():
            if usuario.cpf.valor == cpf:
                logger.debug(f"Usuario encontrado: {usuario.id}")
                return usuario
        logger.debug("Usuario não encontrado")
        return None

    def listar_todos(self) -> List[Usuario]:
        """Lista todos os usuários.

        Returns:
            Lista de usuários
        """
        self._log_operacao("Listando", "Usuários")
        usuarios = list(self.usuarios.values())
        logger.debug(f"Total de usuários: {len(usuarios)}")
        return usuarios

    def listar_ativos(self) -> List[Usuario]:
        """Lista apenas usuários ativos.

        Returns:
            Lista de usuários ativos
        """
        logger.info("Listando usuários ativos")
        ativos = [u for u in self.usuarios.values() if u.ativo]
        logger.debug(f"Usuários ativos: {len(ativos)}")
        return ativos

    def deletar(self, usuario: Usuario) -> None:
        """Deleta um usuário.

        Args:
            usuario: Usuario a deletar
        """
        self._log_operacao("Deletando", "Usuario")
        if usuario.id in self.usuarios:
            del self.usuarios[usuario.id]
            logger.debug(f"Usuario {usuario.id} deletado")

    def contar(self) -> int:
        """Conta total de usuários.

        Returns:
            Total de usuários
        """
        total = len(self.usuarios)
        logger.debug(f"Total de usuários no repositório: {total}")
        return total
