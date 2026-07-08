# Capítulo 14

# O Módulo Settings

---

## Objetivo do Capítulo

Neste capítulo será apresentada a implementação do módulo responsável pelo gerenciamento das configurações globais do PPP Expert IA.

Ao final deste capítulo o leitor compreenderá:

- por que utilizar um módulo centralizado de configurações;
- como funciona o Pydantic Settings;
- como os valores padrão são utilizados;
- como o arquivo `.env` interfere na configuração da aplicação;
- como acessar as configurações em qualquer módulo do sistema.

---

# O Problema

Em aplicações pequenas é comum encontrar código semelhante ao exemplo abaixo.

```python
import os

language = os.getenv("LANGUAGE")
```

Em outro módulo:

```python
database = os.getenv("DATABASE")
```

Depois:

```python
log_level = os.getenv("LOG_LEVEL")
```

À medida que o sistema cresce, dezenas de módulos passam a acessar diretamente as variáveis de ambiente.

Esse modelo apresenta diversos problemas:

- duplicação de código;
- ausência de validação;
- dificuldade para testes;
- elevado acoplamento.

---

# A Solução

O PPP Expert IA adota uma abordagem diferente.

Toda a configuração da aplicação passa por um único módulo.

```
Arquivo .env

        │

        ▼

Settings

        │

        ▼

Demais módulos
```

Nenhum outro módulo conhece o arquivo `.env`.

Todos utilizam exclusivamente:

```python
from core.config.settings import settings
```

---

# A Classe Settings

O módulo é baseado na biblioteca **Pydantic Settings v2**.

Essa biblioteca oferece diversos recursos importantes.

Entre eles:

- leitura automática do arquivo `.env`;
- leitura das variáveis de ambiente;
- validação automática dos tipos;
- conversão automática de dados.

Assim, um valor armazenado como texto no arquivo `.env` pode ser convertido automaticamente para inteiro, booleano ou enumeração.

---

# Valores Padrão

Os valores padrão não são definidos dentro do módulo `settings.py`.

Eles permanecem centralizados em:

```
core/config/defaults.py
```

Esse princípio recebe o nome de **Single Source of Truth**, ou Fonte Única da Verdade.

A vantagem é simples:

Sempre que um valor padrão precisar ser alterado, apenas um arquivo deverá ser modificado.

---

# Organização da Classe

A classe `Settings` foi organizada em blocos.

```
Settings

│

├── Ambiente

├── Configuração Geral

├── Banco de Dados

├── Logging

├── Upload

├── Documentos

├── Configuração do Pydantic

└── Propriedades
```

Essa organização facilita a leitura e padroniza todos os módulos do núcleo da aplicação.

---

# Instância Global

Ao final do módulo existe apenas uma instância.

```python
settings = Settings()
```

Essa instância deverá ser utilizada por toda a aplicação.

Não existe necessidade de criar novos objetos `Settings`.

---

# Exemplo de Utilização

```python
from core.config.settings import settings

print(settings.language)
print(settings.environment)
print(settings.log_level)
```

O módulo consumidor não precisa conhecer:

- arquivo `.env`;
- variáveis de ambiente;
- biblioteca Pydantic.

Toda essa complexidade permanece encapsulada.

---

# Responsabilidade Única

Durante o desenvolvimento foi adotado o princípio da Responsabilidade Única (SRP).

O módulo `Settings` possui apenas uma responsabilidade:

> disponibilizar as configurações da aplicação.

Ele não estabelece conexões com banco de dados.

Não cria diretórios.

Não gera documentos.

Não implementa regras de negócio.

Essas responsabilidades pertencem a outros módulos.

---

# Lições Aprendidas

A implementação deste módulo reforçou alguns princípios importantes de engenharia de software.

- Centralização das configurações.
- Fonte única da verdade.
- Baixo acoplamento.
- Alta coesão.
- Utilização de bibliotecas consolidadas em vez de soluções próprias.

Esses princípios servirão de base para todos os módulos desenvolvidos posteriormente.

---

# Resumo

Ao término deste capítulo o PPP Expert IA passou a possuir uma infraestrutura de configuração robusta, reutilizável e facilmente expansível.

Os próximos módulos utilizarão diretamente a instância global `settings`, tornando o restante do sistema mais simples, organizado e consistente.
