---
capitulo: 7
titulo: Camadas de Negócio com Logging Estruturado
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Capítulo do Livro
pacote: CF-005.03
---

# Camadas de Negócio com Logging Estruturado

## Introdução

Até agora, implementamos a infraestrutura base da aplicação: configuração 
centralizada, logging estruturado e inicialização segura.

Agora começamos a construir as camadas que implementam regras de negócio: 
Domain e Application.

Neste capítulo, veremos como adicionar logging a essas camadas de forma 
elegante, usando classes base que fornecem logging automático.

---

## A Arquitetura de Camadas

Nossa aplicação segue Clean Architecture com três camadas principais:

```
┌──────────────────────────┐
│   Application Layer      │ ← Casos de Uso, Serviços
├──────────────────────────┤
│     Domain Layer         │ ← Entidades, ValueObjects
├──────────────────────────┤
│     Core Layer           │ ← Configuração, Logger
└──────────────────────────┘
```

**Domain Layer** contém:
- Entidades (representam conceitos do negócio)
- Value Objects (valores imutáveis)
- Repositories (interfaces de persistência)

**Application Layer** contém:
- Use Cases (orquestram lógica de negócio)
- Services (operações reutilizáveis)

**Core Layer** contém:
- Configuration (settings, environment)
- Logger (infrastructure de logging)

---

## Entidades: Representando Conceitos

Uma entidade é um objeto que tem identidade única e pode mudar ao longo 
do tempo.

### Exemplo: Usuário

```python
from src.domain.entities import Entity

class Usuario(Entity):
    def __init__(self, nome: str, email: str):
        super().__init__(nome=nome, email=email)
        self.nome = nome
        self.email = email
```

Simples! Ao criar um usuário:

```python
usuario = Usuario(nome="Werner", email="werner@example.com")
# Log automático:
# INFO  | Entity Usuario created
# DEBUG | Attributes: ['nome', 'email']
```

### Por Que Logging em __init__?

Permite rastreamento de quando objetos são criados:

- ✅ Debug: "Quando este usuário foi criado?"
- ✅ Auditoria: "Quem criou quantos usuários?"
- ✅ Performance: "Estamos criando muitos objetos?"

### Herança Automática

Todas as subclasses herdam logging:

```python
class Produto(Entity):
    pass

class Categoria(Entity):
    pass

produto = Produto(nome="Notebook", preco=2000)
# INFO  | Entity Produto created
# DEBUG | Attributes: ['nome', 'preco']
```

Sem adicionar logging manualmente!

---

## Value Objects: Valores Imutáveis

Um value object representa um valor que não muda. Dois value objects com 
os mesmos dados são considerados iguais.

### Exemplo: Email

```python
from src.domain.value_objects import ValueObject

class Email(ValueObject):
    def __init__(self, endereco: str):
        super().__init__(endereco)

# Uso
email1 = Email("werner@example.com")
email2 = Email("werner@example.com")

email1 == email2  # True! Mesmo conteúdo = iguais
```

### Por Que Value Objects?

Encapsulam validação e comportamento:

```python
class Email(ValueObject):
    def __init__(self, endereco: str):
        if "@" not in endereco:
            raise ValueError("Email inválido")
        super().__init__(endereco)
```

Agora, sempre que você tem um Email, você sabe que é válido!

### Características Fornecidas

A classe base ValueObject fornece:

1. **Igualdade (`==`)**: Compara por valor
2. **Hashable (`hash()`)**: Pode usar em sets/dicts
3. **Representação (`repr()`)**: Para logging
4. **Imutabilidade**: Via `@property valor`

```python
# Igualdade
email1 = Email("werner@example.com")
email2 = Email("werner@example.com")
assert email1 == email2  # ✅

# Hashable
emails = {email1, email2}
assert len(emails) == 1  # Conjunto remove duplicatas

# Imutabilidade
email1.valor = "outro@example.com"  # ❌ AttributeError
```

---

## Services: Operações Reutilizáveis

Um serviço encapsula lógica que não pertence a uma entidade específica.

### Exemplo: Serviço de Saudação

```python
from src.application.services import Service

class SaudacaoService(Service):
    def executar(self, nome: str, sobrenome: str):
        return f"Olá, {nome} {sobrenome}!"

# Uso
servico = SaudacaoService()
resultado = servico("Werner", "Schindel")
# INFO  | Serviço SaudacaoService iniciado
# DEBUG | Parâmetros: {...}
# INFO  | Serviço SaudacaoService concluído com sucesso
```

### Logging Automático

O `__call__` intercepta a chamada e adiciona logging:

1. Log de início (INFO)
2. Log de parâmetros (DEBUG)
3. Executar a lógica
4. Log de conclusão (INFO)
5. Log de erro (ERROR, se houver)

Sem você fazer nada!

### Exemplo Real: Serviço de Criptografia

```python
class CriptografiaService(Service):
    def executar(self, texto: str, chave: str):
        # Lógica de criptografia
        return texto_criptografado

# Ao chamar:
servico = CriptografiaService()
resultado = servico(texto="senha123", chave="minhachave")

# Logs:
# INFO  | Serviço CriptografiaService iniciado
# DEBUG | Parâmetros: {'kwargs': {'texto': 'se...', 'chave': 'me...'}}
# INFO  | Serviço CriptografiaService concluído com sucesso
```

Note que os parâmetros são truncados (primeiros 50 caracteres) para não 
poluir logs com dados muito grandes.

---

## Use Cases: Orquestração de Negócio

Um caso de uso representa uma operação completa de negócio. Ele orquestra 
entidades, value objects e serviços.

### Exemplo: Criar Usuário

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
        # 1. Validar entrada
        if not requisicao.nome:
            return UsuarioCriadoResponse(
                sucesso=False,
                mensagem="Nome é obrigatório"
            )
        
        # 2. Criar entidade
        usuario = Usuario(
            nome=requisicao.nome,
            email=requisicao.email
        )
        
        # 3. Persistir (seria chamada a repository aqui)
        usuario_id = self.repository.salvar(usuario)
        
        # 4. Retornar resultado
        return UsuarioCriadoResponse(
            sucesso=True,
            mensagem="Usuário criado com sucesso",
            usuario_id=usuario_id
        )

# Uso
caso = CriarUsuarioUseCase()
requisicao = CriarUsuarioRequest(
    nome="Werner",
    email="werner@example.com"
)
resposta = caso(requisicao)

# Logs:
# INFO  | Caso de Uso CriarUsuarioUseCase iniciado
# DEBUG | Requisição: CriarUsuarioRequest
# INFO  | Entity Usuario created
# DEBUG | Attributes: ['nome', 'email']
# INFO  | Caso de Uso CriarUsuarioUseCase concluído: True
# DEBUG | Mensagem: Usuário criado com sucesso
```

### Por Que Use Cases?

Separação clara entre:
- **Lógica de apresentação** (controllers, views)
- **Lógica de negócio** (use cases)
- **Lógica de persistência** (repositories)

Facilita testes, mudanças e manutenção.

---

## Padrão de Herança

Todas as classes base fornecem logging automático via herança:

```
Entity                      Service
  ↑                           ↑
  │ herda                      │ herda
  │                            │
Usuario                   CriptografiaService
Produto                   ValidacaoService
Categoria                 EnvioEmailService

ValueObject                UseCase
  ↑                          ↑
  │ herda                     │ herda
  │                           │
Email                    CriarUsuarioUseCase
CPF                      AlterarSenhaUseCase
CEP                      EnviarInviteUseCase
```

Quando você cria uma subclasse, logging é automático!

---

## Exemplo Completo: Sistema de Cadastro

Vamos ver como tudo funciona junto:

```python
# 1. Definir value objects
class Email(ValueObject):
    def __init__(self, endereco: str):
        if "@" not in endereco:
            raise ValueError("Email inválido")
        super().__init__(endereco)

# 2. Definir entidade
class Usuario(Entity):
    def __init__(self, nome: str, email: Email):
        super().__init__(nome=nome, email=email)
        self.nome = nome
        self.email = email

# 3. Definir caso de uso
@dataclass
class CadastrarRequest(UseCaseRequest):
    nome: str
    email: str

class CadastrarUseCase(UseCase):
    def executar(self, req: CadastrarRequest):
        # Validação via ValueObject
        email = Email(req.email)  # Pode lançar ValueError
        
        # Criar entidade
        usuario = Usuario(nome=req.nome, email=email)
        
        # Persistir
        id = self.repository.salvar(usuario)
        
        return UseCaseResponse(
            sucesso=True,
            mensagem="Cadastro realizado"
        )

# 4. Executar
caso = CadastrarUseCase()
resultado = caso(CadastrarRequest(
    nome="Werner",
    email="werner@example.com"
))

# Logs automáticos rastreiam toda operação!
```

---

## Nos Bastidores: Decisões de Design

### Por Que Logging em __call__ e não __init__?

Para Service e UseCase, logging em `__call__` e não `__init__` porque:

- ✅ Criação do serviço não é o evento interessante
- ✅ Execução do serviço é o evento que importa
- ✅ Logging no `__init__` ocorreria apenas uma vez (criação)
- ✅ Logging no `__call__` ocorre a cada execução (uso real)

```python
# Isto não seria útil
servico = CriptografiaService()  # Log: Serviço criado
# (nada entre meio)
# ... semanas depois ...

# Isto é útil!
resultado = servico(texto="dados")  # Log: Serviço executado
resultado = servico(texto="mais")   # Log: Serviço executado
resultado = servico(texto="etc")    # Log: Serviço executado
```

### Por Que ValueObject com Igualdade?

Em um banco de dados, objetos diferentes representam linhas diferentes.
No domínio, dois objetos com os mesmos dados são iguais:

```python
# Banco de dados
usuario1 = repository.buscar_por_id(1)  # Usuário id=1
usuario2 = repository.buscar_por_id(1)  # Usuário id=1 (diferente, mas mesmo dado)

usuario1 is usuario2  # False (objetos diferentes)
usuario1 == usuario2  # True (dados iguais) - porque Entity pode ter __eq__

# Value objects
email1 = Email("werner@example.com")
email2 = Email("werner@example.com")

email1 is email2  # False (objetos diferentes)
email1 == email2  # True (valores iguais) - ValueObject implementa __eq__
```

---

## Erros Comuns a Evitar

### ❌ Não faça:

1. **Misturar lógica em Entity**
   ```python
   class Usuario(Entity):
       def enviar_email(self):  # ❌ Use um Service
           pass
   ```

2. **Criar UseCase com muita responsabilidade**
   ```python
   class CadastroUseCase(UseCase):  # ❌ Responsabilidade única!
       def executar(self, req):
           # Criar usuário
           # Enviar email
           # Registrar log
           # Enviar SMS
           # ... 500 linhas
   ```

3. **Esquecer de herdar das classes base**
   ```python
   class MinhaEntidade:  # ❌ Logging manual!
       def __init__(self, dados):
           logger.info("Entidade criada")  # Não herda
           self.dados = dados
   ```

### ✅ Faça:

1. **Entidades para estado, Services para comportamento**
   ```python
   class Usuario(Entity):
       pass  # Apenas dados
   
   class EnvioEmailService(Service):
       def executar(self, usuario):
           # Lógica de envio
   ```

2. **Use Cases simples e focados**
   ```python
   class CriarUsuarioUseCase(UseCase):  # Uma coisa
       def executar(self, requisicao):
           return resultado
   ```

3. **Herde das classes base sempre**
   ```python
   class MinhaEntidade(Entity):  # Logging automático!
       pass
   ```

---

## Testando Domain e Application

Como testar com logging automático?

```python
def test_criar_usuario():
    caso = CriarUsuarioUseCase()
    requisicao = CriarUsuarioRequest(
        nome="Werner",
        email="werner@example.com"
    )
    resposta = caso(requisicao)
    
    assert resposta.sucesso
    assert resposta.usuario_id is not None
    # Logging é feito automaticamente
```

Os testes **não precisam validar logs**. O logging é automático e 
garantido pela classe base.

---

## Resumo

**Camada Domain:**
- Entidades: Objetos com identidade
- Value Objects: Valores imutáveis e iguais por conteúdo

**Camada Application:**
- Services: Operações reutilizáveis
- Use Cases: Orquestração de negócio

**Logging Automático:**
- Herança fornece logging sem código adicional
- INFO para eventos significativos
- DEBUG para detalhes técnicos

**Próximo Passo:**
No próximo capítulo, criaremos entidades e use cases reais para o sistema PPP.
