---
documento: REQ-0006
titulo: Especificação Técnica — Integração do Logger
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 08/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-005.02
modulo: Integração de logging em múltiplos módulos
---

# Especificação Técnica

## Pacote

CF-005.02 — Integração do Logger

---

# Objetivo

Integrar o logger centralizado (Loguru) aos módulos existentes da camada core, 
adicionando logging estruturado em pontos-chave do ciclo de vida da aplicação.

---

# Motivação

O logger foi implementado em CF-005.01 como singleton encapsulado. Agora é 
necessário validar sua integração em contextos reais, observar o comportamento 
em diferentes ambientes e cenários, e garantir que o logging acontece nos 
momentos apropriados do ciclo de vida.

---

# Escopo

### Módulos a Integrar

1. **environment/environment.py**
   - Log ao carregamento do environment
   - Debug: tipo de environment detectado

2. **src/core/config/defaults.py**
   - Log ao carregamento dos defaults
   - Debug: valores padrão significativos

3. **src/core/config/settings.py**
   - Log ao instanciar Settings
   - Debug: valores carregados do .env
   - Info: environment detectado

4. **src/core/paths.py**
   - Log ao inicializar estrutura de diretórios
   - Debug: caminhos calculados

5. **src/core/version.py**
   - Log ao carregar versão
   - Info: nome e versão da aplicação

### Não estão no escopo

- Criação de novos módulos
- Mudanças na arquitetura
- Alteração de interfaces públicas
- Refatoração de código existente
- Performance optimization

---

# Interface

### Pontos de Logging

#### Ambiente (environment.py)

```python
# Ao carregar o environment
logger.info(f"Environment loaded: {env_name}")
logger.debug(f"Environment type: {type(env).__name__}, Value: {env.value}")
```

#### Defaults (defaults.py)

```python
# Ao carregar o módulo
logger.info("Default configuration loaded")
logger.debug(f"Default log level: {DEFAULT_LOG_LEVEL}")
logger.debug(f"Default database: {DEFAULT_DATABASE_FILENAME}")
```

#### Settings (settings.py)

```python
# Ao instanciar
logger.info("Settings instance created")
logger.debug(f"Current environment: {settings.environment}")

# Ao carregar valores do .env
if os.getenv('LOG_LEVEL'):
    logger.debug(f"LOG_LEVEL from .env: {os.getenv('LOG_LEVEL')}")
```

#### Paths (paths.py)

```python
# Ao inicializar
logger.info("Project paths initialized")
logger.debug(f"Project root: {PROJECT_ROOT}")
logger.debug(f"Source directory: {SRC_DIR}")
```

#### Version (version.py)

```python
# Ao carregar
logger.info(f"Application: {APPLICATION_NAME} v{APPLICATION_VERSION}")
logger.debug(f"Author: {APPLICATION_AUTHOR}")
```

---

# Requisitos de Teste

### Testes Unitários

1. **test_environment_logging**
   - Importar environment module
   - Verificar que logger foi utilizado
   - Capturar mensagens de log
   - Validar conteúdo

2. **test_defaults_logging**
   - Importar defaults module
   - Verificar logs de default
   - Validar tipos de log (info/debug)

3. **test_settings_logging**
   - Criar instância de Settings
   - Capturar logs de criação
   - Validar ambiente detectado

4. **test_paths_logging**
   - Importar paths module
   - Verificar logs de inicialização
   - Validar caminhos no log

5. **test_version_logging**
   - Importar version module
   - Verificar logs de versão
   - Validar formato esperado

---

# Requisitos Não-Funcionais

### Logging Levels

- **INFO**: Eventos significativos (inicialização, ambiente, versão)
- **DEBUG**: Valores específicos (caminhos, tipos, valores de configuração)
- **WARNING**: Situações inesperadas
- **ERROR**: Erros de carregamento (não esperado nesta fase)

### Performance

- Nenhum impacto perceptível na inicialização
- Overhead negligível

### Compatibilidade

- Sem breaking changes
- Interfaces públicas inalteradas
- Código existente continua funcionando

---

# Dependências

- ✅ CF-005.01 (Logger) — já concluído
- ✅ src/core/config/defaults.py — existente
- ✅ src/core/config/settings.py — existente
- ✅ src/core/paths.py — existente
- ✅ src/core/version.py — existente

---

# Configuração

### Ambientes de Teste

1. **Desenvolvimento**
   - Logs no console com cores
   - Arquivos de log criados em `data/logs/`

2. **Teste (pytest)**
   - Captura de logs via pytest
   - Validação de conteúdo

3. **Produção (conceitual)**
   - Logs apenas em arquivo
   - Sem saída de console

---

# Critérios de Aceição

- [ ] Todos os 5 módulos implementam logging nos pontos específicos
- [ ] Nenhuma regressão (28 testes ainda passam)
- [ ] Logs aparecem nos níveis corretos (INFO/DEBUG)
- [ ] Nenhum circular import
- [ ] Testes unitários capturam e validam mensagens
- [ ] Formatação de logs é consistente

---

# Próximas Fases

Após CF-005.02:

- CF-005.03: Logger em módulos domain
- CF-006: Persistência e SQLAlchemy
- CF-007: Aplicação de casos de uso

---

# Notas Técnicas

### Importação do Logger

```python
from src.core.logging import logger
```

Não há risco de circular import porque logger.py importa Settings 
no tempo de carregamento, e esses módulos (environment, defaults, paths, version) 
não importam Settings.

### Captura de Logs em Testes

```python
def test_something(caplog):
    # caplog é fixture do pytest que captura logs
    logger.info("test message")
    assert "test message" in caplog.text
```

---

# Histórico de Versões

| Versão | Data | Status | Notas |
|--------|------|--------|-------|
| 1.0 | 08/07/2026 | Rascunho | Especificação inicial |

