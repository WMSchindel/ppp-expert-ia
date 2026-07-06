---
documento: CAP-0003
titulo: Constantes, Final e Código Autoexplicativo
autor: Werner Schindel
projeto: PPP Expert IA
versao: 1.0
data: 06/07/2026
status: Concluído
tipo: Capítulo do Livro
---

# Capítulo 3

# Constantes, Final e Código Autoexplicativo

---

# Objetivos

Ao final deste capítulo o leitor será capaz de:

- compreender a importância das constantes em um projeto;
- entender o conceito de código autoexplicativo;
- utilizar `typing.Final`;
- eliminar números mágicos;
- organizar constantes de forma profissional;
- compreender as decisões adotadas no PPP Expert IA.

---

# Introdução

Durante o desenvolvimento de qualquer software surgem valores que não
devem mudar durante a execução da aplicação.

Exemplos:

- idioma padrão;
- codificação padrão;
- tamanho máximo de upload;
- nível de log;
- nome do banco de dados.

Esses valores são chamados de **constantes**.

Embora pareçam simples, sua organização influencia diretamente a
qualidade do software.

---

# O problema dos números mágicos

Considere o seguinte código.

```python
MAX_UPLOAD_SIZE = 52428800
```

O código funciona.

Mas existe um problema.

O que significa o número:

```
52428800
```

50 MB?

50 KB?

50 GB?

Não existe nenhuma indicação.

Esse tipo de valor recebe o nome de **número mágico (Magic Number)**.

---

# Eliminando números mágicos

Uma primeira melhoria seria:

```python
MAX_UPLOAD_SIZE = 50 * 1024 * 1024
```

Agora já conseguimos perceber que existe uma relação com megabytes.

Mas ainda podemos melhorar.

---

# Código Autoexplicativo

No PPP Expert IA adotamos a seguinte abordagem.

```python
KILOBYTE = 1024

MEGABYTE = 1024 * KILOBYTE

MAX_UPLOAD_SIZE = 50 * MEGABYTE
```

Agora o código explica a si próprio.

Não é necessário realizar contas mentalmente.

Essa característica recebe o nome de:

> **Código Autoexplicativo (Self-Documenting Code).**

---

# Organização das Constantes

Todas as constantes foram reunidas em um único módulo.

```
src/

└── core/

    └── config/

        defaults.py
```

Esse módulo tornou-se a única fonte oficial para valores padrão da
aplicação.

---

# Por que não espalhar constantes?

Imagine um projeto contendo:

```
logger.py

database.py

pdf.py

upload.py

api.py
```

Cada módulo poderia definir seus próprios valores.

Isso produziria um efeito conhecido como:

> **Duplicação de Conhecimento**

Se amanhã o tamanho máximo de upload mudar de 50 MB para 100 MB,
quantos arquivos precisarão ser alterados?

Provavelmente vários.

Centralizando as constantes esse problema desaparece.

---

# Utilizando Final

No projeto utilizamos:

```python
from typing import Final
```

e declaramos:

```python
DEFAULT_LANGUAGE: Final[str] = "pt-BR"
```

O uso de `Final` comunica claramente ao leitor que aquele valor deve ser
tratado como constante.

Embora o Python não impeça sua alteração em tempo de execução,
ferramentas de análise estática conseguem detectar modificações
indevidas.

---

# Organização por Domínio

As constantes foram agrupadas por responsabilidade.

```
Unidades de Medida

Configuração Geral

Banco de Dados

Logging

Upload

Documentos
```

Essa organização reduz o tempo necessário para localizar uma
informação.

---

# Responsabilidade Única

Observe que o módulo `defaults.py` possui apenas uma responsabilidade.

Definir valores padrão.

Ele não:

- lê arquivos;
- acessa banco de dados;
- executa lógica de negócio;
- cria diretórios.

Essa decisão segue o princípio:

**SRP (Single Responsibility Principle).**

---

# Testes

Todas as constantes possuem testes automatizados.

Arquivo:

```
tests/unit/core/config/test_defaults.py
```

Foram criados testes para:

- unidades de medida;
- configuração geral;
- banco de dados;
- logging;
- upload;
- documentos.

Essa abordagem garante que alterações futuras não provoquem regressões.

---

# Decisões de Engenharia

Durante a implementação deste módulo foram tomadas algumas decisões.

## Utilizar Final

Objetivo:

Melhorar a documentação do código e facilitar análises estáticas.

---

## Eliminar números mágicos

Objetivo:

Aumentar a legibilidade.

---

## Centralizar constantes

Objetivo:

Eliminar duplicação.

---

## Organizar por domínio

Objetivo:

Facilitar manutenção.

---

# Boas Práticas

✔ Utilize constantes para valores imutáveis.

✔ Elimine números mágicos.

✔ Agrupe constantes relacionadas.

✔ Utilize nomes descritivos.

✔ Centralize valores reutilizados.

✔ Escreva código para pessoas.

---

# Erros Comuns

## Espalhar constantes

Errado:

```python
upload.py

MAX = 50
```

```python
pdf.py

MAX = 50
```

---

## Utilizar números mágicos

Errado:

```python
MAX_UPLOAD = 52428800
```

---

## Misturar responsabilidades

Errado:

```python
defaults.py

def read_env():
    ...
```

O módulo deve conter apenas constantes.

---

# Nos Bastidores do Projeto

Durante a implementação do módulo `defaults.py`, algumas decisões de
engenharia foram discutidas antes da escrita do código.

Inicialmente avaliamos utilizar diretamente:

```python
MAX_UPLOAD_SIZE = 50 * 1024 * 1024
```

Após análise, optamos por criar constantes intermediárias para unidades
de medida (`KILOBYTE`, `MEGABYTE` e `GIGABYTE`).

Essa decisão não alterou o funcionamento do software, mas tornou o
código significativamente mais legível e reutilizável.

Esse é um exemplo de como pequenas decisões podem melhorar a qualidade
de um projeto ao longo do tempo.

---

# Exercícios

1. Explique com suas palavras o que é um número mágico.

2. Reescreva o código abaixo eliminando os números mágicos.

```python
LIMIT = 10485760
```

3. Pesquise a diferença entre `Final` e uma constante convencional.

4. Em quais situações **não** faz sentido utilizar `Final`?

---

# Resumo

Neste capítulo aprendemos:

- o que são constantes;
- o conceito de código autoexplicativo;
- como eliminar números mágicos;
- por que utilizar `typing.Final`;
- como organizar constantes em projetos profissionais;
- as decisões de engenharia adotadas no PPP Expert IA.

---

# Referências

- PEP 8 – Style Guide for Python Code
- PEP 591 – Final Qualifier
- Clean Code – Robert C. Martin
- REQ-CF-004-02 – Defaults
- ER-0002 – Engineering Review
- ADR-0002 – Estratégia de Imports
