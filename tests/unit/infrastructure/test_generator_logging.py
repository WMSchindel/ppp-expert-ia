"""
Testes para logging de geradores.

Valida que geradores fazem logging correto ao serem utilizados.
"""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.infrastructure.generators import Generator


class RelatorioGenerator(Generator):
    """Gerador de exemplo para testes."""

    def gerar(self, dados: dict) -> Path:
        """Gera um relatório."""
        self._log_inicio_geracao("Relatório")

        if not self.output_dir:
            self.output_dir = Path.cwd()

        arquivo = self.output_dir / f"relatorio_{dados.get('nome', 'default')}.txt"

        try:
            # Simula geração de arquivo
            conteudo = f"Relatório\n{dados}\n"
            arquivo.write_text(conteudo)

            self._log_conclusao_geracao(arquivo)
            return arquivo
        except Exception as e:
            self._log_erro_geracao("Relatório", e)
            raise


class PlanilhaGenerator(Generator):
    """Outro gerador de exemplo."""

    def gerar(self, dados: dict) -> Path:
        """Gera uma planilha."""
        self._log_inicio_geracao("Planilha")

        if not self.output_dir:
            self.output_dir = Path.cwd()

        arquivo = self.output_dir / f"planilha.txt"

        conteudo = "Planilha\n" + str(dados)
        arquivo.write_text(conteudo)

        self._log_conclusao_geracao(arquivo)
        return arquivo


def test_generator_can_be_created():
    """Testa que um gerador pode ser criado."""
    with TemporaryDirectory() as tmpdir:
        gen = RelatorioGenerator(Path(tmpdir))
        assert gen is not None


def test_generator_has_logging_support():
    """Testa que Generator fornece suporte a logging."""
    assert hasattr(Generator, '_log_inicio_geracao')
    assert hasattr(Generator, '_log_conclusao_geracao')
    assert hasattr(Generator, '_log_erro_geracao')

    with TemporaryDirectory() as tmpdir:
        gen = RelatorioGenerator(Path(tmpdir))
        assert gen is not None


def test_generator_gera_documento():
    """Testa que um gerador pode gerar documentos."""
    with TemporaryDirectory() as tmpdir:
        gen = RelatorioGenerator(Path(tmpdir))
        dados = {"nome": "test", "conteudo": "dados teste"}

        arquivo = gen.gerar(dados)

        assert arquivo.exists()
        assert arquivo.suffix == ".txt"


def test_generator_conteudo_correto():
    """Testa que o documento gerado tem conteúdo correto."""
    with TemporaryDirectory() as tmpdir:
        gen = RelatorioGenerator(Path(tmpdir))
        dados = {"nome": "test"}

        arquivo = gen.gerar(dados)
        conteudo = arquivo.read_text()

        assert "Relatório" in conteudo
        assert "test" in conteudo


def test_multiple_generators():
    """Testa múltiplos geradores."""
    with TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        gen_rel = RelatorioGenerator(tmppath)
        gen_plan = PlanilhaGenerator(tmppath)

        arquivo1 = gen_rel.gerar({"nome": "rel1"})
        arquivo2 = gen_plan.gerar({"nome": "plan1"})

        assert arquivo1.exists()
        assert arquivo2.exists()
        assert len(list(tmppath.glob("*"))) == 2
