---
documento: REQ-0007
titulo: Especificação Técnica — Logger em Domain Layers
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Em Desenvolvimento
tipo: Especificação Técnica
pacote: CF-005.03
modulo: Domain e Application Layers
---

# Especificação Técnica

## Pacote

CF-005.03 — Logger em Domain Layers

---

# Objetivo

Expandir a cobertura de logging para as camadas domain e application, 
fornecendo observabilidade nas regras de negócio e operações da aplicação.

---

# Motivação

O logger foi integrado com sucesso na camada core (CF-005.02). Agora é 
necessário estender o logging para as camadas de negócio (domain e 
application), permitindo rastreamento de:

- Criação de entidades
- Validações de negócio
- Operações de casos de uso
- Serviços de aplicação

---

# Escopo

### Módulos a Integrar

#### Domain Layer

1. **src/domain/entities/**
   - Logging ao criar entidades
   - Debug: atributos principais
   - Warning: validações falhadas

2. **src/domain/value_objects/**
   - Logging ao criar value objects
   - Debug: valores validados

3. **src/domain/repositories/**
   - Logging ao definir contratos
   - Info: operações iniciadas

#### Application Layer

4. **src/application/services/**
   - Logging ao executar serviços
   - Debug: parâmetros recebidos
   - Info: operações concluídas

5. **src/application/use_cases/**
   - Logging ao iniciar caso de uso
   - Debug: entrada do caso de uso
   - Info: resultado do caso de uso

### Não estão no escopo

- Criação de novos módulos
- Mudanças em interfaces
- Refatoração de lógica
- Alteração de arquitetura

---

# Interface de Logging

### Entidades (Domain)

```python
# entities/base_entity.py
class Entity:
    def __init__(self, **kwargs):
        logger.info(f"Entity {self.__class__.__name__} created")
        logger.debug(f"Attributes: {kwargs}")
```

### Value Objects (Domain)

```python
# value_objects/base_value_object.py
class ValueObject:
    def __init__(self, value):
        logger.debug(f"ValueObject {self.__class__.__name__}: {value}")
```

### Services (Application)

```python
# services/base_service.py
class Service:
    def execute(self, *args, **kwargs):
        logger.info(f"Service {self.__class__.__name__} started")
        logger.debug(f"Parameters: {kwargs}")
        # ... lógica
        logger.info(f"Service {self.__class__.__name__} completed")
```

### Use Cases (Application)

```python
# use_cases/base_use_case.py
class UseCase:
    def execute(self, request):
        logger.info(f"UseCase {self.__class__.__name__} started")
        logger.debug(f"Request: {request}")
        # ... lógica
        logger.info(f"UseCase {self.__class__.__name__} completed")
```

---

# Requisitos de Teste

### Testes Unitários

1. **test_entity_logging**
   - Criar entidade
   - Validar que logger foi chamado
   - Validar mensagens

2. **test_value_object_logging**
   - Criar value object
   - Validar logging

3. **test_service_logging**
   - Executar serviço
   - Validar logging de início e fim

4. **test_use_case_logging**
   - Executar caso de uso
   - Validar logging completo

### Cobertura

- Todas as classes base devem ter logging
- Pelo menos um exemplo de cada tipo
- 100% de testes passando
- Sem regressões nos 35 testes existentes

---

# Requisitos Não-Funcionais

### Logging Levels

- **INFO**: Operações significativas (criação, início/fim)
- **DEBUG**: Detalhes técnicos (parâmetros, valores)
- **WARNING**: Validações falhadas
- **ERROR**: Erros de negócio

### Performance

- Sem impacto perceptível
- Logging estruturado e eficiente

### Compatibilidade

- Sem breaking changes
- Interfaces públicas inalteradas
- Padrão consistente com CF-005.02

---

# Arquitetura de Integração

```
┌─ Core Layer (CF-005.02) ✅
│  └─ Initializer coordena logging
│
├─ Domain Layer (CF-005.03) ← AQUI
│  ├─ Entities
│  ├─ ValueObjects
│  └─ Repositories
│
├─ Application Layer (CF-005.03) ← AQUI
│  ├─ Services
│  └─ UseCases
│
└─ Infrastructure Layer
   └─ Persistence, Generators, etc
```

---

# Padrão de Implementação

### Base Classes com Logging

Cada camada terá uma classe base que encapsula logging:

```python
# domain/entities/base_entity.py
from src.core.logging import logger

class Entity:
    def __init__(self):
        logger.info(f"{self.__class__.__name__} created")

# domain/value_objects/base_value_object.py
class ValueObject:
    def __init__(self, value):
        logger.debug(f"{self.__class__.__name__} initialized")
```

### Herança Automática

Subclasses herdam logging automaticamente:

```python
class User(Entity):  # herda logging do Entity
    pass

class Email(ValueObject):  # herda logging do ValueObject
    pass
```

---

# Dependências

- ✅ CF-005.01 (Logger) — centralizado
- ✅ CF-005.02 (Integration) — lazy init
- ✅ src/domain/* — estrutura base
- ✅ src/application/* — estrutura base

---

# Critérios de Aceição

- [ ] Todas as classes base têm logging
- [ ] Pelo menos 1 entidade com teste de logging
- [ ] Pelo menos 1 service com teste de logging
- [ ] Pelo menos 1 use case com teste de logging
- [ ] Nenhuma regressão (35+ testes passando)
- [ ] Sem circular imports
- [ ] Documentação técnica concluída
- [ ] Engineering review positiva

---

# Próximas Fases

CF-005.04 — Logger em Infrastructure Layer
- Logging em persistência
- Logging em generators
- Logging em parsers

---

# Notas Técnicas

### Evitar Over-logging

Não adicione logging em:
- Métodos privados (prefixo `_`)
- Getters/setters simples
- Loops internos (pode ser verboso)

### Níveis Apropriados

- INFO: O que aconteceu (positivo)
- DEBUG: Como aconteceu (detalhes)
- WARNING: Algo inesperado
- ERROR: Erro de negócio

---

# Histórico de Versões

| Versão | Data | Status | Notas |
|--------|------|--------|-------|
| 1.0 | 09/07/2026 | Rascunho | Especificação inicial |
