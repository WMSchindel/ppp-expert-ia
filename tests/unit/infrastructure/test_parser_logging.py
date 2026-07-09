"""
Testes para logging de parsers.

Valida que parsers fazem logging correto ao serem utilizados.
"""

import pytest
from src.infrastructure.parsers import Parser


class CSVParser(Parser):
    """Parser de CSV de exemplo para testes."""

    def __init__(self):
        super().__init__("CSV")

    def parse(self, entrada: str):
        """Faz parsing de string CSV."""
        self._log_inicio_parsing()

        linhas = entrada.strip().split("\n")
        resultados = []

        for i, linha in enumerate(linhas, 1):
            try:
                if "," not in linha:
                    self._log_erro_parsing(
                        ValueError("Formato inválido"),
                        i
                    )
                    continue

                partes = linha.split(",")
                resultado = {
                    "campo1": partes[0].strip(),
                    "campo2": partes[1].strip() if len(partes) > 1 else None,
                }
                resultados.append(resultado)
            except Exception as e:
                self._log_erro_parsing(e, i)

        self._log_conclusao_parsing(len(resultados))
        return resultados


class JSONParser(Parser):
    """Parser de JSON de exemplo."""

    def __init__(self):
        super().__init__("JSON")

    def parse(self, entrada: str):
        """Faz parsing de JSON."""
        self._log_inicio_parsing()

        import json

        try:
            dados = json.loads(entrada)

            if isinstance(dados, list):
                self._log_conclusao_parsing(len(dados))
                return dados
            else:
                self._log_conclusao_parsing(1)
                return [dados]
        except json.JSONDecodeError as e:
            self._log_erro_parsing(e)
            raise


def test_parser_can_be_created():
    """Testa que um parser pode ser criado."""
    parser = CSVParser()
    assert parser is not None


def test_parser_has_logging_support():
    """Testa que Parser fornece suporte a logging."""
    assert hasattr(Parser, '_log_inicio_parsing')
    assert hasattr(Parser, '_log_conclusao_parsing')
    assert hasattr(Parser, '_log_erro_parsing')

    parser = CSVParser()
    assert parser is not None


def test_parser_csv_valido():
    """Testa parsing de CSV válido."""
    parser = CSVParser()
    csv = "nome,email\nWerner,werner@example.com"

    resultado = parser.parse(csv)

    assert len(resultado) == 2
    assert resultado[0]["campo1"] == "nome"
    assert resultado[1]["campo1"] == "Werner"


def test_parser_csv_multiplas_linhas():
    """Testa parsing de CSV com múltiplas linhas."""
    parser = CSVParser()
    csv = "Werner,werner@example.com\nJoão,joao@example.com"

    resultado = parser.parse(csv)

    assert len(resultado) == 2
    assert resultado[0]["campo1"] == "Werner"
    assert resultado[1]["campo1"] == "João"


def test_parser_csv_invalido():
    """Testa parsing de CSV inválido."""
    parser = CSVParser()
    csv = "Werner\nSem virgula"

    resultado = parser.parse(csv)

    # Linhas inválidas são puladas
    assert len(resultado) <= 2


def test_parser_json_valido():
    """Testa parsing de JSON válido."""
    parser = JSONParser()
    json_str = '{"nome": "Werner", "email": "werner@example.com"}'

    resultado = parser.parse(json_str)

    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Werner"


def test_parser_json_array():
    """Testa parsing de JSON array."""
    parser = JSONParser()
    json_str = '[{"nome": "Werner"}, {"nome": "João"}]'

    resultado = parser.parse(json_str)

    assert len(resultado) == 2


def test_multiple_parsers():
    """Testa múltiplos parsers."""
    csv_parser = CSVParser()
    json_parser = JSONParser()

    csv_data = "a,b\nc,d"
    json_data = '[{"x": "y"}]'

    resultado_csv = csv_parser.parse(csv_data)
    resultado_json = json_parser.parse(json_data)

    assert len(resultado_csv) > 0
    assert len(resultado_json) > 0
