---
documento: CAP-0005
titulo: Logger e Loguru
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Capítulo do Livro
---

# Capítulo 5

# Logger e Loguru

---

# Objetivos

Ao final deste capítulo o leitor será capaz de:

- compreender a importância de um logger centralizado;
- entender como o Loguru funciona;
- integrar o logger com o sistema de configuração;
- utilizar o logger em seus próprios módulos;
- compreender as decisões arquiteturais do PPP Expert IA.

---

# Introdução

Quando um software começa a funcionar em produção, uma pergunta crucial surge:

> Como saber o que está acontecendo quando algo dá errado?

A resposta é: **logging**.

Um logger é um sistema que registra eventos ocorridos na aplicação: operações 
bem-sucedidas, avisos, erros e informações de depuração.

Sem logging apropriado, quando um erro ocorre em produção, você fica cego.

---

# O Problema Sem Logger Centralizado

Considere uma aplicação onde cada módulo implementa seu próprio logging.

Módulo A pode usar:

```python
print("Erro!")
```

Módulo B pode usar:

```python
import logging
logging.error("Erro!")
```

Módulo C pode usar:

```python
with open("app.log", "a") as f:
    f.write("Erro!\n")
```

Problemas óbvios:

- Inconsistência no formato das mensagens.
- Dificuldade em comparar logs de diferentes módulos.
- Falta de controle centralizado sobre níveis e rotação.
- Código duplicado em toda a aplicação.

---

# A Solução: Logger Centralizado

No PPP Expert IA, criamos um único módulo responsável por todo o logging:

```text
core/logging/logger.py
```

Todos os módulos fazem o mesmo:

```python
from core.logging.logger import logger

logger.info("Operação concluída")
logger.error("Erro na operação")
logger.debug("Informação de depuração")
```

Benefícios:

- Consistência garantida;
- Configuração centralizada;
- Fácil manutenção;
- Mensagens estruturadas.

---

# O Que é Loguru?

Loguru é uma biblioteca Python que simplifica drasticamente o logging.

Comparação com a biblioteca padrão `logging`:

### logging (padrão)

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Mensagem")
```

### Loguru

```python
from loguru import logger

logger.info("Mensagem")
```

Loguru fornece:

- configuração mais simples;
- formatação melhor;
- rotação automática de arquivos;
- suporte a múltiplos handlers;
- tratamento de exceções automático.

---

# Arquitetura do Logger no PPP Expert IA

```text
Configuração (Settings)
         ↓
    Logger Core
         ↓
    ┌────┴────┐
    ↓         ↓
Console    Arquivo
(colorido) (completo)
```

O logger lê as configurações do `Settings`:

- Nível de log
- Tamanho máximo do arquivo
- Tempo de retenção

Depois configura dois handlers:

1. **Console**: para desenvolvimento, com cores
2. **Arquivo**: para produção, com todas as informações

---

# Como o Logger é Configurado

Quando você importa o logger:

```python
from core.logging.logger import logger
```

Internamente:

1. O módulo `logger.py` é carregado.
2. A função `_configure_logger()` é chamada automaticamente.
3. Os handlers são criados e configurados.
4. Uma instância global é exportada.

---

# Usando o Logger

No PPP Expert IA, você usa o logger assim:

```python
from core.logging.logger import logger

# Informação
logger.info("Aplicação iniciada")

# Aviso
logger.warning("Recurso em falta")

# Erro
logger.error("Falha ao conectar ao banco")

# Debug
logger.debug("Valor da variável: {}", valor)

# Sucesso
logger.success("Operação concluída")

# Crítico
logger.critical("Sistema indisponível")
```

---

# Formatos de Mensagem

As mensagens incluem automaticamente:

```
2026-07-09 14:32:45.123 | INFO     | core.config.settings:45 | Aplicação iniciada
2026-07-09 14:32:46.456 | ERROR    | infrastructure.database:123 | Falha ao conectar
```

Componentes:

- **Timestamp**: quando o evento ocorreu
- **Nível**: severidade (INFO, ERROR, etc.)
- **Módulo:função:linha**: onde o log foi gerado
- **Mensagem**: o que aconteceu

---

# Rotação Automática de Arquivos

O Loguru cuida automaticamente de:

- Criar novo arquivo quando atinge o tamanho máximo
- Deletar logs antigos automaticamente
- Manter a estrutura dos arquivos organizada

Configuração vem de `defaults.py`:

```python
DEFAULT_LOG_ROTATION = "10 MB"
DEFAULT_LOG_RETENTION = "30 days"
```

---

# Boas Práticas

✅ Sempre use o logger centralizado

Correto:

```python
from core.logging.logger import logger

logger.error("Erro ao processar")
```

❌ Evite implementar seu próprio logging

Errado:

```python
print("Erro!")  # Não faz assim
```

---

# Erros Comuns

## Importar Loguru Diretamente

Errado:

```python
from loguru import logger

logger.info("Mensagem")
```

Correto:

```python
from core.logging.logger import logger

logger.info("Mensagem")
```

---

## Não Incluir Contexto nas Mensagens

Errado:

```python
logger.error("Erro!")  # Muito genérico
```

Correto:

```python
logger.error("Erro ao conectar ao banco: {}", str(e))
```

---

# Nos Bastidores do Projeto

Durante a implementação do logger, enfrentamos uma decisão importante:

**Deveria o logger ser um singleton ou uma class?**

Inicialmente consideramos permitir múltiplas instâncias.

Após análise, adotamos o singleton (instância única) porque:

- Toda a aplicação precisa de um logger consistente
- Uma instância global centraliza a configuração
- Reduz duplicação de código
- Facilita debugging

Essa decisão reflete um princípio mais amplo: **encapsular a complexidade**.

O usuário não precisa saber que Loguru existe. Ele importa `logger` e pronto.

---

# Resumo

Neste capítulo aprendemos:

- por que um logger centralizado é importante;
- como o Loguru simplifica o logging;
- a arquitetura do logger no PPP Expert IA;
- como usar o logger corretamente;
- boas práticas e erros comuns.

---

# Exercícios

1. Abra o arquivo `src/core/logging/logger.py` e estude como o Loguru é configurado.

2. Crie um pequeno script que use o logger com todos os níveis de severidade.

3. Altere o arquivo `.env` para definir `LOG_LEVEL=DEBUG` e observe a diferença.

4. Explique com suas palavras por que um logger centralizado é melhor que cada 
   módulo implementar seu próprio.

---

# Referências

- REQ-0004 — Logger
- ER-0005 — Engineering Review
- Documentação do Loguru
- src/core/logging/logger.py
