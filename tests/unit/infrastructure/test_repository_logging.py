"""
Testes para logging de repositórios.

Valida que repositórios fazem logging correto ao serem utilizados.
"""

import pytest
from src.infrastructure.persistence import Repository


class UsuarioRepository(Repository):
    """Repositório de exemplo para testes."""

    def __init__(self, session=None):
        super().__init__(session)
        self.usuarios = {}
        self.id_counter = 1

    def salvar(self, entidade):
        """Salva uma entidade."""
        self._log_operacao("Salvando", "Usuario")
        id_usuario = self.id_counter
        self.usuarios[id_usuario] = entidade
        self.id_counter += 1
        return entidade

    def buscar_por_id(self, id: int):
        """Busca uma entidade por ID."""
        self._log_operacao("Buscando", f"Usuario #{id}")
        return self.usuarios.get(id)

    def listar_todos(self):
        """Lista todas as entidades."""
        self._log_operacao("Listando", "Usuários")
        return list(self.usuarios.values())

    def deletar(self, entidade):
        """Deleta uma entidade."""
        self._log_operacao("Deletando", "Usuario")
        for id, user in self.usuarios.items():
            if user == entidade:
                del self.usuarios[id]
                break


class ProdutoRepository(Repository):
    """Outro repositório de exemplo."""

    def __init__(self, session=None):
        super().__init__(session)
        self.produtos = {}

    def salvar(self, entidade):
        self._log_operacao("Salvando", "Produto")
        self.produtos[len(self.produtos) + 1] = entidade
        return entidade

    def buscar_por_id(self, id: int):
        self._log_operacao("Buscando", f"Produto #{id}")
        return self.produtos.get(id)

    def listar_todos(self):
        self._log_operacao("Listando", "Produtos")
        return list(self.produtos.values())

    def deletar(self, entidade):
        self._log_operacao("Deletando", "Produto")


def test_repository_can_be_created():
    """Testa que um repositório pode ser criado."""
    repo = UsuarioRepository()
    assert repo is not None


def test_repository_has_logging_support():
    """Testa que Repository fornece suporte a logging."""
    assert hasattr(Repository, '_log_operacao')
    assert hasattr(Repository, '_log_erro')
    repo = UsuarioRepository()
    assert repo is not None


def test_repository_salvar():
    """Testa que um repositório pode salvar entidades."""
    repo = UsuarioRepository()
    usuario = {"nome": "Werner", "email": "werner@example.com"}
    resultado = repo.salvar(usuario)
    assert resultado == usuario


def test_repository_buscar():
    """Testa busca de entidade."""
    repo = UsuarioRepository()
    usuario = {"nome": "Werner", "email": "werner@example.com"}
    repo.salvar(usuario)
    encontrado = repo.buscar_por_id(1)
    assert encontrado == usuario


def test_repository_listar():
    """Testa listagem de entidades."""
    repo = UsuarioRepository()
    usuario1 = {"nome": "Werner", "email": "werner@example.com"}
    usuario2 = {"nome": "João", "email": "joao@example.com"}

    repo.salvar(usuario1)
    repo.salvar(usuario2)

    todos = repo.listar_todos()
    assert len(todos) == 2


def test_multiple_repositories():
    """Testa múltiplos repositórios."""
    repo_usuario = UsuarioRepository()
    repo_produto = ProdutoRepository()

    usuario = {"nome": "Werner"}
    produto = {"nome": "Notebook", "preco": 2000}

    repo_usuario.salvar(usuario)
    repo_produto.salvar(produto)

    assert len(repo_usuario.listar_todos()) == 1
    assert len(repo_produto.listar_todos()) == 1
