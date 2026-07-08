---
documento: ENG-0002
titulo: Diário de Engenharia - Defaults
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 06/07/2026
status: Concluído
tipo: Diário de Engenharia
pacote: CF-004.02
modulo: src/core/config/defaults.py
---

# Diário de Engenharia

## Pacote

CF-004.02

---

# Objetivo da Sessão

Implementar o módulo `defaults.py`, responsável por centralizar todos os
valores padrão utilizados pela aplicação.

O objetivo secundário foi estabelecer um padrão para definição de
constantes, eliminando números mágicos e adotando código
autoexplicativo.

---

# Atividades Executadas

- Implementação do módulo `defaults.py`.
- Definição das constantes globais da aplicação.
- Organização das constantes por domínio funcional.
- Criação dos testes unitários.
- Execução da suíte completa de testes.
- Atualização da documentação técnica.
- Produção do capítulo do livro referente ao módulo.

---

# Estrutura Implementada

O módulo foi organizado em seis grupos.

- Unidades de Medida
- Configuração Geral
- Banco de Dados
- Logging
- Upload
- Documentos

Essa organização melhora a legibilidade e facilita futuras ampliações.

---

# Decisões Técnicas

## Utilização de `Final`

Foi adotado `typing.Final` em todas as constantes para indicar que seus
valores não devem ser modificados durante a execução da aplicação.

Essa decisão melhora a documentação do código e permite verificações por
ferramentas de análise estática.

---

## Eliminação de Números Mágicos

Optou-se por substituir valores numéricos literais por constantes
intermediárias.

Exemplo:

```python
MAX_UPLOAD_SIZE = 50 * MEGABYTE
```

Essa abordagem torna o código mais legível.

---

## Organização por Domínio

As constantes foram agrupadas por responsabilidade.

Essa organização reduz o tempo necessário para localizar uma constante e
facilita futuras manutenções.

---

# Problemas Encontrados

Durante a execução da suíte de testes foi identificado um teste
desatualizado.

Arquivo:

```text
tests/unit/core/test_version.py
```

O teste esperava:

```python
0.1.0
```

Enquanto a versão atual da aplicação passou a ser:

```python
0.1.0-alpha
```

Além disso, o teste ainda utilizava o padrão antigo de imports
(`from src.core...`), contrariando a ADR-0002.

---

# Solução Adotada

O teste foi atualizado para:

- utilizar imports absolutos (`from core...`);
- validar a versão `0.1.0-alpha`.

Após a correção, toda a suíte foi executada novamente com sucesso.

---

# Lições Aprendidas

- Testes também precisam evoluir quando os requisitos mudam.
- Constantes bem organizadas reduzem a dívida técnica.
- Código autoexplicativo melhora a manutenção.
- Pequenas decisões de arquitetura geram benefícios ao longo do projeto.

---

# Melhorias Identificadas

Avaliar futuramente a criação de um módulo específico para constantes
compartilhadas, caso haja reutilização significativa.

Exemplo:

```text
core/constants/
```

No momento, essa alteração não é necessária.

---

# Próximo Pacote

CF-004.03

Implementação do módulo:

```text
src/core/config/settings.py
```

---

# Observações

Este pacote consolidou o padrão de desenvolvimento para módulos de
constantes.

As decisões tomadas neste módulo servirão como referência para futuros
componentes da aplicação.

---

# Situação

Pacote concluído tecnicamente.

Restam apenas as atualizações administrativas do projeto:

- SPRINT_001.md
- STATUS_DO_PROJETO.md
- CONTINUAR_PROJETO.md
- CHANGELOG.md
- Commit Git
