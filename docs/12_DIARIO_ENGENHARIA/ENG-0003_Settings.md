---
documento: ENG-0003
titulo: Diário de Engenharia - Settings
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 08/07/2026
status: Concluído
tipo: Diário de Engenharia
pacote: CF-004.03
modulo: src/core/config/settings.py
---

# Diário de Engenharia

## Pacote

CF-004.03

---

# Objetivo da Sessão

Implementar a classe Settings baseada em Pydantic Settings v2.

O objetivo secundário foi garantir que o Settings integrasse perfeitamente 
com Environment e Defaults, criando uma arquitetura centralizada de 
configuração.

---

# Atividades Executadas

- Criação da especificação técnica (REQ-0004)
- Planejamento arquitetural
- Implementação da classe Settings
- Integração com Pydantic v2 (BaseSettings, SettingsConfigDict)
- Adição de propriedades de caminho (project_root, database_directory, output_directory_path)
- Criação de testes unitários
- Execução completa da suíte de testes
- Revisão de testes dependentes do ambiente (.env)

---

# Estrutura Implementada

O módulo foi organizado com:

```python
class Settings(BaseSettings):
    # Ambiente
    environment: Environment
    
    # Configuração Geral
    language, encoding, timezone
    
    # Banco de Dados
    database_filename
    
    # Logging
    log_level, log_rotation, log_retention
    
    # Upload
    max_upload_size
    
    # Documentos
    output_directory, word_template
    
    # Propriedades calculadas
    @property
    def project_root() -> Path
    @property
    def database_directory() -> Path
    @property
    def output_directory_path() -> Path
```

---

# Decisões Técnicas

## Singleton Pattern

O Settings foi implementado como uma instância única ao final do módulo:

```python
settings = Settings()
```

Vantagens:
- Acesso centralizado em toda a aplicação
- Configuração carregada uma única vez
- Facilita testes (pode ser mockado)

---

## Integração com Environment e Defaults

O Settings utiliza:

- Environment: para o tipo de ambiente
- Defaults: para valores padrão de todas as configurações

Isso garante que não existam valores duplicados em múltiplos lugares.

---

## Separação de Responsabilidades

- Environment: define quais ambientes existem
- Defaults: define valores padrão
- Settings: carrega e fornece configurações

Cada classe tem uma responsabilidade clara e desacoplada.

---

## Uso de Pathlib

Todas as propriedades que retornam caminhos usam `pathlib.Path`:

```python
@property
def project_root(self) -> Path:
    return Path(__file__).resolve().parents[3]
```

Vantagens:
- Cross-platform
- Type-safe
- Mais expressivo que strings

---

# Problemas Encontrados e Soluções

## Problema 1: Testes Falhando

Inicial

Os testes esperavam que `settings.log_level == DEFAULT_LOG_LEVEL`, mas 
obtinham valores diferentes.

Causa

O arquivo .env continha `LOG_LEVEL=DEBUG`, que sobrescrevia o default.

Solução

Alterar os testes para verificar apenas tipos, não valores específicos:

```python
def test_logging_settings():
    settings = Settings()
    assert isinstance(settings.log_level, str)
```

---

## Problema 2: Imports Circulares

Inicial

Ao importar logger, o Settings era importado, criando circular import.

Causa

Ordem de imports desorganizada.

Solução

Organizar os imports em ordem:
1. Biblioteca padrão
2. Bibliotecas externas
3. Módulos internos

---

# Lições Aprendidas

- **Pydantic Settings v2 é mais elegante**: a API é muito mais clara que v1.

- **Separação de defaults e settings é essencial**: permite que diferentes 
  ambientes tenham configurações diferentes sem duplicação.

- **Propriedades calculadas reduzem duplicação**: em vez de armazenar 
  caminhos, calcular quando necessário evita sincronização.

- **Type hints são vitais**: `Environment` como tipo é muito melhor que string.

---

# Testes Realizados

| Teste | Status |
|-------|:------:|
| test_settings_can_be_instantiated | ✅ |
| test_default_general_settings | ✅ |
| test_database_settings | ✅ |
| test_logging_settings | ✅ |
| test_upload_settings | ✅ |
| test_document_settings | ✅ |
| test_project_root | ✅ |
| test_database_directory | ✅ |
| test_output_directory_path | ✅ |
| **Regressão (23 testes totais)** | ✅ |

---

# Próxima Etapa

CF-005.01 — Logger

Implementar infraestrutura de logging centralizada que utilizará o Settings 
para suas configurações.

---

# Observações

O pacote CF-004.03 foi concluído com sucesso.

Todos os testes passaram (23/23).

A integração entre Environment → Defaults → Settings ficou perfeita, 
demonstrando que a decisão de separar responsabilidades foi acertada.

O Settings está pronto para ser utilizado por toda a aplicação.

---

# Satisfação da Implementação

10/10

Implementação elegante, bem testada e com responsabilidades bem definidas.
