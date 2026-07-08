---
documento: REQ-0004
titulo: Especificação Técnica - Logger
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Aprovado
tipo: Especificação Técnica
pacote: CF-005.01
modulo: src/core/logging/logger.py
---

# REQ-0004

# Especificação Técnica

## Módulo `logger.py`

---

# Objetivo

Implementar a infraestrutura de logging centralizada da aplicação utilizando 
Loguru, encapsulando toda a complexidade de configuração em um único módulo.

O logger será a Única interface utilizada por toda a aplicação para registrar 
eventos, erros e informações de depuração.

---

# Motivação

Sem um logger centralizado, cada módulo tende a:

- implementar seu próprio sistema de logs;
- gerar saída inconsistente;
- dificultar depuração do sistema completo;
- desperdiçar tempo configurando logging em múltiplos locais.

O módulo `logger.py` centraliza essa responsabilidade e fornece uma interface 
simples e consistente para toda a aplicação.

---

# Escopo

Este módulo será responsável por:

- criar e configurar o logger global;
- integrar com as configurações definidas em `settings.py`;
- disponibilizar uma interface única para logging;
- gerenciar rotação e retenção de logs;
- suportar múltiplos níveis de severidade.

---

# Não Faz Parte do Escopo

O módulo não deverá:

- processar logs;
- analisar logs;
- armazenar logs em banco de dados;
- enviar logs para serviços remotos (por enquanto);
- criar alertas baseados em logs.

---

# Dependências

## Biblioteca padrão

- sys
- pathlib

## Bibliotecas externas

- loguru

## Módulos internos

- core.config.settings
- core.config.defaults
- core.paths

---

# Interface Pública

O módulo disponibilizará:

```python
logger
```

Uma instância única (singleton) do logger configurado e pronto para uso.

Exemplo de uso:

```python
from core.logging.logger import logger

logger.info("Mensagem de informação")
logger.error("Mensagem de erro")
logger.debug("Mensagem de depuração")
```

---

# Configurações Suportadas

O logger será configurado com base em:

| Configuração | Origem | Padrão |
|--------------|--------|--------|
| Nível | `settings.log_level` | INFO |
| Rotação | `settings.log_rotation` | 10 MB |
| Retenção | `settings.log_retention` | 30 days |
| Diretório | `settings.logs_path` | data/logs |

---

# Níveis de Log Suportados

- DEBUG
- INFO
- SUCCESS
- WARNING
- ERROR
- CRITICAL

---

# Formato das Mensagens

As mensagens de log incluirão:

- Timestamp
- Nível de severidade
- Nome do módulo
- Número da linha
- Mensagem

Exemplo:

```
2026-07-09 14:32:45.123 | INFO     | core.config.settings:45 | Aplicação iniciada
2026-07-09 14:32:46.456 | ERROR    | infrastructure.database:123 | Falha ao conectar
```

---

# Saída do Logger

O logger será configurado para:

1. **Console**: exibir logs com cores e formatação legível
2. **Arquivo**: armazenar logs completos no diretório `data/logs`

---

# Critérios de Aceitação

O módulo será considerado concluído quando:

- possuir uma classe ou função para inicializar o logger;
- estar integrado com `settings.py`;
- possuir testes unitários aprovados;
- possuir testes de integração com Console e Arquivo;
- estar documentado;
- possuir exemplo de uso no livro.

---

# Casos de Teste

| ID | Descrição |
|----|-----------|
| CT-001 | Logger pode ser importado e instanciado |
| CT-002 | Logger registra mensagens no console |
| CT-003 | Logger registra mensagens em arquivo |
| CT-004 | Logger respeita o nível configurado em settings |
| CT-005 | Logger rotaciona arquivos quando atinge o tamanho máximo |
| CT-006 | Logger retém logs apenas pelo tempo configurado |
| CT-007 | Logger é thread-safe |

---

# Riscos

O principal risco é a perda de logs importantes devido a configuração inadequada 
de retenção ou rotação. Portanto, os padrões serão conservadores e bem testados.

---

# Evoluções Futuras

Futuras expansões do logger poderão incluir:

- integração com serviços de logging remotos (Sentry, ELK);
- análise automática de logs;
- alertas baseados em padrões;
- dashboard de monitoramento;
- integração com APM (Application Performance Monitoring).

Essas funcionalidades somente serão implementadas quando houver necessidade real.

---

# Referências

- Documentação do Loguru
- Defaults (log_level, log_rotation, log_retention)
- Settings (configurações globais)
- Paths (localização de diretórios)
- Arquitetura do PPP Expert IA
