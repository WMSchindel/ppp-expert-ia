---
documento: INFRASTRUCTURE_LOGGING
titulo: Documentação Técnica — Logging em Infrastructure Layer
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Documentação Técnica
pacote: CF-005.04
---

# Logging em Infrastructure Layer

## Objetivo

Documentar a arquitetura de logging para a camada de infraestrutura que 
coordena persistência, geração de documentos e processamento de dados.

---

## Arquitetura

```
┌─────────────────────────────────────────┐
│     Infrastructure Layer (CF-005.04)    │
│  ├─ Persistence (Repository)            │
│  ├─ Generators (Documento, Planilha)    │
│  └─ Parsers (CSV, JSON, etc)            │
└─────────────────────────────────────────┘
              ↑
┌─────────────────────────────────────────┐
│      Application Layer (CF-005.03)      │
│  ├─ Services                            │
│  └─ Use Cases                           │
└─────────────────────────────────────────┘
              ↑
┌─────────────────────────────────────────┐
│        Domain Layer (CF-005.03)         │
│  ├─ Entities                            │
│  └─ ValueObjects                        │
└─────────────────────────────────────────┘
              ↑
┌─────────────────────────────────────────┐
│         Core Layer (CF-005.01/02)       │
│  ├─ Logger (Loguru)                     │
│  └─ Configuration                       │
└─────────────────────────────────────────┘
```

---

## Repository: Persistência

**Classe Base:** `Repository[T]`

**Localização:** `src/infrastructure/persistence/base_repository.py`

### Implementação

```python
from src.infrastructure.persistence import Repository

class UsuarioRepository(Repository):
    def __init__(self, session=None):
        super().__init__(session)
        # Repository inicializado com logging

    def salvar(self, usuario):
        self._log_operacao("Salvando", "Usuario")
        # ... lógica
        return usuario

    def buscar_por_id(self, id):
        self._log_operacao("Buscando", f"Usuario #{id}")
        # ... lógica
        return usuario

    def listar_todos(self):
        self._log_operacao("Listando", "Usuários")
        # ... lógica
        return usuarios

    def deletar(self, usuario):
        self._log_operacao("Deletando", "Usuario")
        # ... lógica
```

### Logging Automático

- ✅ INFO: Inicialização do repositório
- ✅ INFO: Operações (salvar, buscar, listar, deletar)
- ✅ ERROR: Erros durante operações

### Métodos Auxiliares

```python
_log_operacao(operacao, entidade_nome)
    # Log: "Salvando: Usuario"

_log_erro(operacao, entidade_nome, erro)
    # Log: "Erro ao salvar Usuario: ..."
```

---

## Generator: Geração de Documentos

**Classe Base:** `Generator`

**Localização:** `src/infrastructure/generators/base_generator.py`

### Implementação

```python
from pathlib import Path
from src.infrastructure.generators import Generator

class DocumentoWordGenerator(Generator):
    def __init__(self, output_dir: Path):
        super().__init__(output_dir)
        # Generator inicializado com logging

    def gerar(self, dados: dict) -> Path:
        self._log_inicio_geracao("Documento Word")

        try:
            arquivo = self._criar_documento(dados)
            self._log_conclusao_geracao(arquivo)
            return arquivo
        except Exception as e:
            self._log_erro_geracao("Documento Word", e)
            raise
```

### Logging Automático

- ✅ INFO: Inicialização do gerador
- ✅ INFO: Início da geração
- ✅ DEBUG: Tipo de documento
- ✅ DEBUG: Diretório de saída
- ✅ INFO: Conclusão
- ✅ DEBUG: Caminho e tamanho do arquivo
- ✅ ERROR: Erros durante geração

### Métodos Auxiliares

```python
_log_inicio_geracao(tipo_documento)
    # Log: "Iniciando geração de Documento Word"
    # Log: "Diretório de saída: /caminho"

_log_conclusao_geracao(caminho_arquivo)
    # Log: "Documento gerado com sucesso"
    # Log: "Arquivo: /caminho/documento.docx"
    # Log: "Tamanho: 125.50 KB"

_log_erro_geracao(tipo_documento, erro)
    # Log: "Erro ao gerar Documento Word: ..."
```

---

## Parser: Processamento de Dados

**Classe Base:** `Parser`

**Localização:** `src/infrastructure/parsers/base_parser.py`

### Implementação

```python
from src.infrastructure.parsers import Parser

class CSVParser(Parser):
    def __init__(self):
        super().__init__("CSV")
        # Parser inicializado com logging

    def parse(self, arquivo: str):
        self._log_inicio_parsing(arquivo)

        resultados = []
        erros = 0

        for i, linha in enumerate(linhas, 1):
            try:
                registro = self._parse_linha(linha)
                resultados.append(registro)
            except Exception as e:
                self._log_erro_parsing(e, i)
                erros += 1

        self._log_conclusao_parsing(len(resultados))
        self._log_validacao(len(resultados), erros)
        return resultados
```

### Logging Automático

- ✅ INFO: Inicialização do parser
- ✅ INFO: Início do parsing
- ✅ DEBUG: Tipo de entrada
- ✅ DEBUG: Arquivo (se aplicável)
- ✅ INFO: Conclusão
- ✅ DEBUG: Quantidade de registros
- ✅ ERROR: Erros por linha
- ✅ WARNING: Registros inválidos

### Métodos Auxiliares

```python
_log_inicio_parsing(arquivo=None)
    # Log: "Iniciando parsing de CSV"
    # Log: "Arquivo: dados.csv"

_log_conclusao_parsing(quantidade)
    # Log: "Parsing concluído com sucesso"
    # Log: "Registros processados: 1000"

_log_erro_parsing(erro, linha=None)
    # Log: "Erro ao fazer parsing na linha 5: ..."

_log_validacao(validos, invalidos)
    # Log: "Registros válidos: 995"
    # Log: "Registros inválidos: 5" (se houver)
```

---

## Padrão de Logging

### Níveis

| Nível | Uso | Exemplo |
|-------|-----|---------|
| INFO | Eventos | "Salvando: Usuario", "Gerando documento", "Parsing concluído" |
| DEBUG | Detalhes | "Diretório: /path", "Linhas: 100", "Tamanho: 125 KB" |
| WARNING | Inesperado | "Registros inválidos: 5" |
| ERROR | Erro | "Erro ao salvar Usuario: ...", "Erro ao fazer parsing: ..." |

### Exemplo de Logs Completos

```
# Repository
2026-07-09 15:30:00.123 | INFO  | Repositório UsuarioRepository inicializado
2026-07-09 15:30:01.234 | INFO  | Salvando: Usuario
2026-07-09 15:30:01.235 | INFO  | Usuario salvo com sucesso

# Generator
2026-07-09 15:30:02.345 | INFO  | Gerador DocumentoGenerator inicializado
2026-07-09 15:30:02.346 | INFO  | Iniciando geração de Documento Word
2026-07-09 15:30:02.347 | DEBUG | Diretório de saída: /data/output
2026-07-09 15:30:03.456 | INFO  | Documento gerado com sucesso
2026-07-09 15:30:03.457 | DEBUG | Arquivo: /data/output/documento.docx
2026-07-09 15:30:03.458 | DEBUG | Tamanho: 125.50 KB

# Parser
2026-07-09 15:30:04.567 | INFO  | Parser CSVParser inicializado
2026-07-09 15:30:04.568 | INFO  | Iniciando parsing de CSV
2026-07-09 15:30:04.569 | DEBUG | Arquivo: dados.csv
2026-07-09 15:30:05.678 | INFO  | Parsing concluído com sucesso
2026-07-09 15:30:05.679 | DEBUG | Registros processados: 1000
2026-07-09 15:30:05.680 | DEBUG | Registros válidos: 995
2026-07-09 15:30:05.681 | WARNING | Registros inválidos: 5
```

---

## Testes

### Cobertura

| Módulo | Testes | Status |
|--------|--------|:------:|
| Repository | 6 | ✅ |
| Generator | 6 | ✅ |
| Parser | 7 | ✅ |
| **Total** | **19** | **✅** |

### Estratégia

1. **Criação:** Objeto pode ser criado
2. **Logging:** Objeto fornece suporte a logging
3. **Operações:** Métodos funcionam
4. **Integração:** Múltiplos objetos trabalham juntos

---

## Integração com Arquitetura

### Fluxo Completo

```
1. UseCase chama Repository
   └─ Repository.salvar(entidade)
      └─ logger.info("Salvando: Usuario")

2. Service chama Generator
   └─ Generator.gerar(dados)
      └─ logger.info("Iniciando geração")

3. UseCase chama Parser
   └─ Parser.parse(entrada)
      └─ logger.info("Iniciando parsing")
```

### Sem Circular Imports

Todas as classes base importam logger após ser inicializado:

```python
# OK - logger já foi inicializado
from src.core.logging import logger

class Repository:
    def __init__(self):
        logger.info("Repository criado")
```

---

## Boas Práticas

✅ **Faça:**
```python
class UsuarioRepository(Repository):
    def salvar(self, usuario):
        self._log_operacao("Salvando", "Usuario")
```

❌ **Evite:**
```python
class UsuarioRepository(Repository):
    def salvar(self, usuario):
        for item in usuario.dados:
            logger.info(f"Processando {item}")  # Over-logging
```

---

## Troubleshooting

### "Logger not found"

**Causa:** Logger não foi inicializado

**Solução:** Chamar `initialize_application()` antes

```python
from src.initializer import initialize_application

initialize_application()
repo = UsuarioRepository()  # Agora funciona
```

### Logs não aparecem

**Causa:** Log level pode ser muito alto

**Solução:** Verificar settings

```python
from src.core.config.settings import settings
print(f"Log level: {settings.log_level}")  # Deve ser INFO ou DEBUG
```

---

## Próximas Fases

CF-006 — Primeira Entidade Real (Usuario PPP)

Objetivo: Criar entidade real do domínio com repository correspondente.

---

## Referências

- [[LOGGING.md]](LOGGING.md) — Core logger
- [[LOGGING_INTEGRATION.md]](LOGGING_INTEGRATION.md) — Lazy initialization
- [[DOMAIN_APPLICATION_LOGGING.md]](DOMAIN_APPLICATION_LOGGING.md) — Domain/App
- [[REQ-0008_Infrastructure_Logger.md]](../05_REQUISITOS/REQ-0008_Infrastructure_Logger.md) — Especificação
