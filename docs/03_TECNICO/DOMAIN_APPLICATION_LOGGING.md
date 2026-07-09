---
documento: DOMAIN_APPLICATION_LOGGING
titulo: Documentação Técnica — Logging em Camadas Domain e Application
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Documentação Técnica
pacote: CF-005.03
---

# Logging em Camadas Domain e Application

## Objetivo

Documentar a arquitetura de logging para as camadas de negócio (domain e 
application) da aplicação PPP Expert IA.

---

## Arquitetura

```
┌─────────────────────────────────────────┐
│         Infrastructure Layer            │
│   (Persistence, Generators, etc)        │
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
│  ├─ ValueObjects                        │
│  └─ Repositories (interfaces)           │
└─────────────────────────────────────────┘
              ↑
┌─────────────────────────────────────────┐
│        Core Layer (CF-005.02)           │
│  ├─ Logger (Loguru)                     │
│  ├─ Configuration                       │
│  └─ Initializer                         │
└─────────────────────────────────────────┘
```

---

## Domain Layer

### Entidades (src/domain/entities/)

**Classe Base:** `Entity`

```python
from src.domain.entities import Entity

class Usuario(Entity):
    def __init__(self, nome: str, email: str):
        super().__init__(nome=nome, email=email)
        self.nome = nome
        self.email = email
```

**Logging Automático:**
- ✅ INFO: Criação de entidade
- ✅ DEBUG: Atributos inicializados

**Exemplo de Log:**
```
2026-07-09 10:15:30.123 | INFO  | Entity Usuario created
2026-07-09 10:15:30.124 | DEBUG | Attributes: ['nome', 'email']
```

### Objetos de Valor (src/domain/value_objects/)

**Classe Base:** `ValueObject`

```python
from src.domain.value_objects import ValueObject

class Email(ValueObject):
    def __init__(self, endereco: str):
        super().__init__(endereco)
```

**Logging Automático:**
- ✅ DEBUG: Criação de value object
- ✅ DEBUG: Tipo de valor

**Características Incluídas:**
- Igualdade (`__eq__`)
- Hashable (`__hash__`)
- Imutabilidade (`value` como property)

**Exemplo de Log:**
```
2026-07-09 10:15:30.125 | DEBUG | ValueObject Email criado
2026-07-09 10:15:30.126 | DEBUG | Tipo de valor: str
```

---

## Application Layer

### Serviços (src/application/services/)

**Classe Base:** `Service`

```python
from src.application.services import Service

class SaudacaoService(Service):
    def executar(self, nome: str):
        return f"Olá, {nome}!"

# Uso
servico = SaudacaoService()
resultado = servico("Werner")  # Chama __call__ com logging
```

**Logging Automático:**
- ✅ INFO: Início do serviço
- ✅ DEBUG: Parâmetros recebidos
- ✅ INFO: Conclusão com sucesso
- ✅ ERROR: Exceções capturadas

**Exemplo de Log:**
```
2026-07-09 10:15:30.127 | INFO   | Serviço SaudacaoService iniciado
2026-07-09 10:15:30.128 | DEBUG  | Parâmetros: {'kwargs': {'nome': 'Werner'}}
2026-07-09 10:15:30.129 | INFO   | Serviço SaudacaoService concluído com sucesso
```

### Casos de Uso (src/application/use_cases/)

**Classes Base:**
- `UseCaseRequest`: Requisição base
- `UseCaseResponse`: Resposta base
- `UseCase`: Coordenador

```python
from dataclasses import dataclass
from src.application.use_cases import UseCase, UseCaseRequest, UseCaseResponse

@dataclass
class CriarUsuarioRequest(UseCaseRequest):
    nome: str
    email: str

@dataclass
class UsuarioCriadoResponse(UseCaseResponse):
    usuario_id: int = None

class CriarUsuarioUseCase(UseCase):
    def executar(self, requisicao: CriarUsuarioRequest):
        # Lógica de negócio
        return UsuarioCriadoResponse(
            sucesso=True,
            mensagem="Usuário criado",
            usuario_id=123
        )

# Uso
caso = CriarUsuarioUseCase()
requisicao = CriarUsuarioRequest(nome="Werner", email="werner@example.com")
resposta = caso(requisicao)  # Chama __call__ com logging
```

**Logging Automático:**
- ✅ INFO: Início do caso de uso
- ✅ DEBUG: Tipo da requisição
- ✅ INFO: Conclusão com status
- ✅ DEBUG: Mensagem de resposta
- ✅ ERROR: Exceções capturadas

**Exemplo de Log:**
```
2026-07-09 10:15:30.130 | INFO   | Caso de Uso CriarUsuarioUseCase iniciado
2026-07-09 10:15:30.131 | DEBUG  | Requisição: CriarUsuarioRequest
2026-07-09 10:15:30.132 | INFO   | Caso de Uso CriarUsuarioUseCase concluído: True
2026-07-09 10:15:30.133 | DEBUG  | Mensagem: Usuário criado
```

---

## Padrões de Logging

### Níveis Apropriados

| Nível | Uso | Exemplo |
|-------|-----|---------|
| INFO | Eventos significativos | "Entity Usuario created" |
| DEBUG | Detalhes técnicos | "Attributes: ['nome', 'email']" |
| WARNING | Situações inesperadas | "Validação falhou" |
| ERROR | Erros de negócio | "Email duplicado" |

### Boas Práticas

✅ **Faça:**
```python
logger.info(f"Entity {self.__class__.__name__} created")
logger.debug(f"Atributos: {list(kwargs.keys())}")
```

❌ **Evite:**
```python
# Logging em métodos privados
def _processar(self):
    logger.debug("processando")

# Over-logging em loops
for item in lista:
    logger.info(f"Processando {item}")  # Muito verboso
```

---

## Testes

### Cobertura

| Módulo | Testes | Status |
|--------|--------|:------:|
| Entity | 4 | ✅ |
| ValueObject | 5 | ✅ |
| Service | 6 | ✅ |
| UseCase | 6 | ✅ |
| **Total** | **21** | **✅** |

### Tipos de Testes

1. **Criação:** Entidade/VO/Service/UseCase pode ser criado
2. **Métodos:** Interfaces funcionam corretamente
3. **Logging:** Logging é feito automaticamente
4. **Chamada:** Objetos podem ser chamados (quando aplicável)
5. **Integração:** Múltiplos objetos funcionam juntos

---

## Herança e Composição

### Entity → Subclasses

```python
class Entity:
    def __init__(self, **kwargs):
        logger.info(f"Entity {self.__class__.__name__} created")

class Usuario(Entity):  # Herda logging automático
    pass

class Produto(Entity):  # Herda logging automático
    pass
```

### ValueObject → Subclasses

```python
class ValueObject:
    def __init__(self, valor):
        logger.debug(f"ValueObject {self.__class__.__name__} criado")

class Email(ValueObject):  # Herda logging automático
    pass

class Cpf(ValueObject):  # Herda logging automático
    pass
```

### Service → Subclasses

```python
class Service:
    def __call__(self, *args, **kwargs):
        logger.info(f"Serviço {self.__class__.__name__} iniciado")
        # ... mais logging

class SaudacaoService(Service):  # Herda logging automático
    def executar(self, nome):
        return f"Olá, {nome}!"
```

---

## Integração com Core

O logging de domain e application usa a infraestrutura de core:

1. **Logger centralizado** (CF-005.01)
   - Loguru encapsulado em `src.core.logging`

2. **Lazy initialization** (CF-005.02)
   - `initialize_application()` coordena startup

3. **Configuração** (CF-005)
   - Settings fornece log_level, log_rotation, etc

**Fluxo:**
```
1. Core modules importados (sem logging)
2. initialize_application() chamado
3. Domain/App classes importadas
4. Domain/App classes fazem logging ao serem usadas
5. Tudo vai para console (dev) + arquivo (prod)
```

---

## Performance

- **Impacto na criação:** < 0.1ms por entidade
- **Impacto na execução:** < 1ms por serviço/usecase
- **Logging estruturado:** Sem serialização cara

---

## Troubleshooting

### "Logger not found"

**Causa:** Logger não foi inicializado

**Solução:** Chamar `initialize_application()` antes de usar domain/app

```python
from src.initializer import initialize_application
from src.domain.entities import Entity

initialize_application()  # Isto primeiro!

usuario = Entity()  # Agora funciona
```

### Logs não aparecem

**Causa:** Log level pode estar muito alto

**Solução:** Verificar settings

```python
from src.core.config.settings import settings
print(f"Log level: {settings.log_level}")  # Deve ser INFO ou DEBUG
```

---

## Próximas Fases

CF-005.04 — Logger em Infrastructure Layer
- Logging em persistência
- Logging em generators/parsers

---

## Referências

- [[LOGGING.md]](LOGGING.md) — Core logger
- [[LOGGING_INTEGRATION.md]](LOGGING_INTEGRATION.md) — Lazy initialization
- [[REQ-0007_Domain_Logger.md]](../05_REQUISITOS/REQ-0007_Domain_Logger.md) — Especificação
