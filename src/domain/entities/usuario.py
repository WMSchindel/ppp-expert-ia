"""
Entidade Usuario do domínio PPP.

Representa um usuário do sistema que cria e mantém
Perfis Profissiográficos Previdenciários.
"""

from datetime import datetime
from typing import Optional
from src.domain.entities.base_entity import Entity
from src.domain.value_objects.email import Email
from src.domain.value_objects.cpf import CPF
from src.core.logging import logger


class Usuario(Entity):
    """Entidade que representa um usuário PPP.

    Atributos:
        id: Identificador único
        nome: Nome completo
        email: Email (value object)
        cpf: CPF (value object)
        empresa: Empresa onde trabalha
        cargo: Cargo/função
        data_criacao: Quando foi criado
        ativo: Status do usuário
    """

    def __init__(
        self,
        nome: str,
        email: Email,
        cpf: CPF,
        empresa: str,
        cargo: str,
        id: Optional[int] = None,
        ativo: bool = True,
        data_criacao: Optional[datetime] = None,
    ):
        """Inicializa um novo usuario.

        Args:
            nome: Nome completo
            email: Email (Email value object)
            cpf: CPF (CPF value object)
            empresa: Nome da empresa
            cargo: Cargo/função
            id: Identificador (None para novo)
            ativo: Status inicial (padrão: True)
            data_criacao: Data de criação (padrão: agora)

        Raises:
            ValueError: Se dados inválidos
        """
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio")

        if not isinstance(email, Email):
            raise ValueError("Email deve ser um Email value object")

        if not isinstance(cpf, CPF):
            raise ValueError("CPF deve ser um CPF value object")

        if not empresa or not empresa.strip():
            raise ValueError("Empresa não pode ser vazia")

        if not cargo or not cargo.strip():
            raise ValueError("Cargo não pode ser vazio")

        super().__init__(
            id=id,
            nome=nome,
            email=email,
            cpf=cpf,
            empresa=empresa,
            cargo=cargo,
            ativo=ativo,
        )

        self.id = id
        self.nome = nome.strip()
        self.email = email
        self.cpf = cpf
        self.empresa = empresa.strip()
        self.cargo = cargo.strip()
        self.ativo = ativo
        self.data_criacao = data_criacao or datetime.now()

        logger.debug(f"Usuario criado: {self.nome} ({self.email.valor})")

    def desativar(self) -> None:
        """Desativa o usuário."""
        self.ativo = False
        logger.info(f"Usuario desativado: {self.nome}")

    def atualizar_cargo(self, novo_cargo: str) -> None:
        """Atualiza o cargo do usuário.

        Args:
            novo_cargo: Novo cargo

        Raises:
            ValueError: Se cargo vazio
        """
        if not novo_cargo or not novo_cargo.strip():
            raise ValueError("Cargo não pode ser vazio")

        cargo_anterior = self.cargo
        self.cargo = novo_cargo.strip()
        logger.info(f"Cargo atualizado: {cargo_anterior} → {self.cargo}")

    def atualizar_empresa(self, nova_empresa: str) -> None:
        """Atualiza a empresa do usuário.

        Args:
            nova_empresa: Nova empresa

        Raises:
            ValueError: Se empresa vazia
        """
        if not nova_empresa or not nova_empresa.strip():
            raise ValueError("Empresa não pode ser vazia")

        empresa_anterior = self.empresa
        self.empresa = nova_empresa.strip()
        logger.info(f"Empresa atualizada: {empresa_anterior} → {self.empresa}")

    def __repr__(self) -> str:
        """Representação do usuário."""
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email.valor}')"
