---
documento: ENG-0005
titulo: Diário de Engenharia - Logger
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 09/07/2026
status: Concluído
tipo: Diário de Engenharia
pacote: CF-005.01
modulo: src/core/logging/logger.py
---

# Diário de Engenharia

## Pacote

CF-005.01

---

# Objetivo da Sessão

Implementar a infraestrutura de logging centralizada utilizando Loguru.

O objetivo secundário foi garantir que o logger se integrasse perfeitamente 
com o sistema de configuração (Settings) e seguisse os padrões arquiteturais 
já estabelecidos no projeto.

---

# Atividades Executadas

- Criação da especificação técnica (REQ-0004)
- Planejamento da arquitetura
- Implementação do módulo `logger.py`
- Criação do módulo `__init__.py`
- Implementação dos testes unitários
- Adição da propriedade `logs_path` ao Settings
- Instalação do Loguru
- Execução completa da suíte de testes

---

# Estrutura Implementada

O módulo foi organizado em:

```
src/core/logging/
├── __init__.py       (exporta o logger)
└── logger.py         (implementação)
```

Com testes em:

```
tests/unit/core/logging/
├── __init__.py
└── test_logger.py    (5 testes)
```

---

# Decisões Técnicas

## Singleton Pattern

O logger foi implementado como uma instância única, garantindo que toda a 
aplicação use exatamente a mesma configuração.

Vantagens:
- Coesão arquitetural
- Sem duplicação de configuração
- Mais fácil de manter

---

## Encapsulamento Total do Loguru

O Loguru foi completamente encapsulado dentro do módulo.

A aplicação não precisa saber que Loguru existe:

```python
from core.logging.logger import logger
```

Isso permite futuras migrações para outras bibliotecas sem impacto na 
aplicação.

---

## Dupla Saída

Configuramos dois handlers:

1. **Console**: colorido e legível para desenvolvimento
2. **Arquivo**: completo e estruturado para produção

A integração com Settings permite alterar o comportamento por ambiente.

---

## Criação Automática de Diretórios

O logger cria automaticamente o diretório `data/logs/` se não existir.

```python
settings.logs_path.mkdir(parents=True, exist_ok=True)
```

Isso evita erros ao executar em um ambiente novo.

---

# Problemas Encontrados e Soluções

## Problema 1: Ambiente Virtualizado

Inicial

```
ModuleNotFoundError: No module named 'loguru'
```

Causa

O pytest estava usando um ambiente Python diferente do .venv do projeto.

Solução

Ativar o .venv antes de instalar e executar os testes:

```bash
source .venv/Scripts/activate
```

---

## Problema 2: Propriedade Ausente no Settings

Inicial

O logger tentava acessar `settings.logs_path`, mas a propriedade não existia.

Causa

O Settings não incluía todas as propriedades de caminho necessárias.

Solução

Adicionar a propriedade ao Settings:

```python
@property
def logs_path(self) -> Path:
    """Retorna o diretório de logs."""
    return self.project_root / "data" / "logs"
```

---

# Lições Aprendidas

- **Importância de isolamento de ambientes**: um ambiente virtual bem 
  configurado evita horas de debugging.

- **Integração antecipada**: implementar o logger integrado com Settings 
  desde o início garante que tudo funcione junto.

- **Singleton é apropriado**: para casos de configuração global (logger, 
  database), singleton reduz erros de inconsistência.

- **Encapsulamento liberta**: esconder Loguru permite flexibilidade futura.

---

# Testes Realizados

| Teste | Status |
|-------|:------:|
| test_logger_can_be_imported | ✅ |
| test_logger_has_required_methods | ✅ |
| test_logger_can_log_messages | ✅ |
| test_logger_is_singleton | ✅ |
| test_logger_configuration | ✅ |
| **Regressão (28 testes totais)** | ✅ |

---

# Próxima Etapa

CF-005.02 — Integração do Logger com os Módulos Existentes

Esperado:

- Adicionar logging aos módulos core já existentes
- Validar que o logger funciona em contextos reais
- Possível ajuste fino da configuração

---

# Observações

O pacote CF-005.01 foi concluído com sucesso.

Todos os testes passaram (28/28).

O logger está pronto para ser utilizado por toda a aplicação.

A integração com Settings foi perfeita, demonstrando que a decisão de 
centralizar configurações foi acertada.

---

# Satisfação da Implementação

9/10

O módulo ficou simples, elegante e bem testado. A única razão para não ser 
10/10 é que ainda não testamos o logger em cenários de concorrência (thread 
safety), mas isso será feito quando necessário.
