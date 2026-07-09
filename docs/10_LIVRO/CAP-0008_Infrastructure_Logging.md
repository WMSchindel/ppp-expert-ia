---
capitulo: 8
titulo: Infraestrutura Observável — Repository, Generator, Parser
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Capítulo do Livro
pacote: CF-005.04
---

# Infraestrutura Observável

## Introdução

Com Domain e Application layers implementados, agora focamos na camada que 
faz o trabalho sujo: Infrastructure.

Aqui, persistência, geração de documentos e processamento de dados acontecem. 
Aqui também é onde problemas ocorrem: banco de dados indisponível, arquivo 
grande demais, dados malformados.

Por isso, logging em infraestrutura é crítico.

---

## Repository: Abstração de Persistência

Um Repository encapsula lógica de persistência. Ao invés de espalhá-la pelo 
código, concentramos em uma classe.

```python
from src.infrastructure.persistence import Repository

class UsuarioRepository(Repository):
    def salvar(self, usuario):
        # Logging automático
        # INFO: "Salvando: Usuario"
        
        self.session.add(usuario)
        self.session.commit()
        return usuario
```

### Por Que Logging em Repository?

- ✅ Rastreamento: "O banco salvou isso?"
- ✅ Performance: "Quanto tempo levou?"
- ✅ Debug: "Qual usuario foi salvo?"
- ✅ Auditoria: "Quem salvou quantas vezes?"

---

## Generator: Geração Rastreável

Um Generator cria documentos, planilhas, relatórios. Operações que podem ser:
- Lenta
- Consumir memória
- Falhar por espaço em disco

```python
from src.infrastructure.generators import Generator
from pathlib import Path

class PdfGenerator(Generator):
    def gerar(self, dados: dict) -> Path:
        self._log_inicio_geracao("PDF")
        # ... criando PDF
        self._log_conclusao_geracao(arquivo)
        return arquivo
```

### Logs Úteis

```
Iniciando geração de PDF
Diretório de saída: /data/output
Documento gerado com sucesso
Arquivo: /data/output/relatorio.pdf
Tamanho: 2.5 MB
```

"Ah, o relatório levou 3 segundos e tem 2.5 MB. Normal." ✅

---

## Parser: Parsing Defensivo

Parsers processam dados externos. Sempre há chance de:
- Formato inesperado
- Linhas malformadas
- Caracteres inválidos

```python
from src.infrastructure.parsers import Parser

class CSVParser(Parser):
    def parse(self, arquivo: str):
        self._log_inicio_parsing(arquivo)
        
        for linha in linhas:
            try:
                registro = self._parse_linha(linha)
            except Exception as e:
                self._log_erro_parsing(e, linha_numero)
        
        self._log_conclusao_parsing(len(registros))
        self._log_validacao(validos, invalidos)
```

### Exemplo de Logs

```
Iniciando parsing de CSV
Arquivo: usuarios.csv
Erro ao fazer parsing na linha 5: Formato inválido
Parsing concluído com sucesso
Registros processados: 1000
Registros válidos: 995
Registros inválidos: 5 (WARNING)
```

"5 linhas ruins em 1000. Investigar linha 5." ✅

---

## Integração com Caso de Uso

Vamos ver como tudo funciona junto:

```python
from src.application.use_cases import UseCase
from dataclasses import dataclass

@dataclass
class ImportarUsuariosRequest:
    arquivo: str

class ImportarUsuariosUseCase(UseCase):
    def __init__(self, parser, repository):
        self.parser = parser
        self.repository = repository

    def executar(self, req: ImportarUsuariosRequest):
        # Logs do UseCase
        # INFO: "Caso de Uso ImportarUsuariosUseCase iniciado"
        
        # Logs do Parser
        # INFO: "Iniciando parsing de CSV"
        usuarios = self.parser.parse(req.arquivo)
        
        # Logs do Repository
        # INFO: "Salvando: Usuario" (para cada)
        for usuario in usuarios:
            self.repository.salvar(usuario)
        
        # Logs do UseCase
        # INFO: "Caso de Uso concluído: True"
        
        return UseCaseResponse(
            sucesso=True,
            mensagem=f"Importados {len(usuarios)} usuários"
        )
```

### Logs Completos

```
Caso de Uso ImportarUsuariosUseCase iniciado
Requisição: ImportarUsuariosRequest
Iniciando parsing de CSV
Arquivo: usuarios.csv
Parsing concluído com sucesso
Registros processados: 1000
Registros válidos: 995
Salvando: Usuario (x995)
Usuario salvo com sucesso (x995)
Caso de Uso ImportarUsuariosUseCase concluído: True
Mensagem: Importados 995 usuários
```

Você vê exatamente o que aconteceu! ✅

---

## Padrão: Logging no Ciclo de Vida

Cada classe base segue o mesmo padrão:

```
Inicialização
    ↓
Início da Operação → Parâmetros (DEBUG)
    ↓
Execução
    ↓
Conclusão → Resultado (DEBUG)
    ↓
Erros (se houver)
```

---

## Testes de Integração

Como testar logging em infraestrutura?

```python
def test_repository_com_generator():
    """Teste: Repository salva, Generator cria documento"""
    
    # Criar dados
    usuario = Usuario(nome="Werner")
    
    # Repository salva
    repo = UsuarioRepository()
    repo.salvar(usuario)
    
    # Generator cria relatório
    gen = RelatorioGenerator()
    arquivo = gen.gerar({"usuario": usuario})
    
    # Verificar
    assert arquivo.exists()
    # Logs mostram fluxo completo
```

---

## Nos Bastidores: Decisões

### Por Que Métodos `_log_*` e não direto?

```python
# ❌ Direto (rígido)
class Generator:
    def gerar(self):
        logger.info("Iniciando")
        # ...
        logger.info("Conclusão")

# ✅ Métodos auxiliares (flexível)
class Generator:
    def gerar(self):
        self._log_inicio_geracao()
        # ...
        self._log_conclusao_geracao()
```

A segunda abordagem permite que subclasses customizem logging:

```python
class MeuGerador(Generator):
    def _log_conclusao_geracao(self, arquivo):
        super()._log_conclusao_geracao(arquivo)
        logger.info(f"Enviando para {self.url_destino}")
```

### Por Que Generics em Repository?

```python
class Repository(Generic[T]):
    def salvar(self, entidade: T) -> T:
        pass
```

Type safety:

```python
class UsuarioRepository(Repository[Usuario]):
    def salvar(self, usuario: Usuario) -> Usuario:  # Type hint!
        pass
```

---

## Escalabilidade

À medida que o projeto cresce:

```
Mês 1: 1 Repository, 1 Generator, 1 Parser
Mês 2: 5 Repositories, 3 Generators, 2 Parsers
Mês 3: 20 Repositories, 10 Generators, 5 Parsers

Nenhum problema! Todas herdam logging automaticamente.
```

---

## Resumo

**Repository:** Rastreia persistência  
**Generator:** Rastreia criação de documentos  
**Parser:** Rastreia processamento de dados  

Todas as três fornecem logging automático via herança.

**Resultado:** Sistema completamente observável. 👁️

---

## Próximo Capítulo

Criaremos primeira entidade real do domínio: **Usuario PPP**

Com sua entidade e repository, veremos logging em ação.
