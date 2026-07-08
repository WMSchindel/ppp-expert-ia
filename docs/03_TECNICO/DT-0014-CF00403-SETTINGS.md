# DOCUMENTAÇÃO TÉCNICA

| Campo     | Valor                       |
| --------- | --------------------------- |
| Documento | DT-0014-CF00403-SETTINGS.md |
| Pacote    | CF-004.03                   |
| Módulo    | Settings                    |
| Versão    | 1.0                         |
| Data      | 08/07/2026                  |
| Autor     | Werner Schindel             |

---

# 1. Objetivo

O módulo `settings.py` centraliza todas as configurações utilizadas pelo PPP Expert IA.

Ele fornece um único ponto de acesso para as configurações da aplicação, eliminando dependências diretas de variáveis de ambiente nos demais módulos.

---

# 2. Localização

```
src/
└── core/
    └── config/
        └── settings.py
```

---

# 3. Dependências

O módulo depende de:

```
core.config.environments
```

```
core.config.defaults
```

```
pydantic-settings
```

```
pathlib
```

---

# 4. Estrutura da Classe

A classe `Settings` está organizada em oito blocos.

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

---

# 5. Ambiente

Representa o ambiente de execução da aplicação.

```
development

test

production
```

Tipo:

```python
Environment
```

Valor padrão:

```
DEFAULT_ENVIRONMENT
```

---

# 6. Configuração Geral

São disponibilizados os seguintes parâmetros.

| Atributo | Origem           |
| -------- | ---------------- |
| language | DEFAULT_LANGUAGE |
| encoding | DEFAULT_ENCODING |
| timezone | DEFAULT_TIMEZONE |

---

# 7. Banco de Dados

O módulo disponibiliza:

```
database_filename
```

Origem:

```
DEFAULT_DATABASE_FILENAME
```

O módulo não estabelece conexão com o banco de dados.

Sua responsabilidade limita-se ao armazenamento das configurações.

---

# 8. Logging

São disponibilizados:

```
log_level

log_rotation

log_retention
```

Os valores são provenientes de:

```
defaults.py
```

Podem ser sobrescritos pelo arquivo `.env`.

---

# 9. Upload

Configuração disponível:

```
max_upload_size
```

Origem:

```
MAX_UPLOAD_SIZE
```

---

# 10. Documentos

Configurações:

```
output_directory

word_template
```

---

# 11. Configuração do Pydantic

O módulo utiliza:

```python
SettingsConfigDict
```

Configurações adotadas:

| Parâmetro         | Valor  |
| ----------------- | ------ |
| env_file          | .env   |
| env_file_encoding | utf-8  |
| case_sensitive    | False  |
| extra             | ignore |

---

# 12. Propriedade project_root

Disponibiliza o diretório raiz do projeto.

Retorno:

```python
Path
```

Exemplo:

```python
from core.config.settings import settings

print(settings.project_root)
```

---

# 13. Instância Global

Ao final do módulo é criada uma única instância.

```python
settings = Settings()
```

Todos os módulos da aplicação deverão utilizar exclusivamente essa instância.

Não deverão ser criadas novas instâncias da classe `Settings`, exceto em testes específicos.

---

# 14. Fluxo de Funcionamento

```
Arquivo .env
        │
        ▼
Pydantic Settings
        │
        ▼
Settings
        │
        ▼
Demais módulos
```

---

# 15. Responsabilidades

O módulo possui as seguintes responsabilidades:

- carregar configurações;
- aplicar valores padrão;
- disponibilizar configurações para o restante da aplicação.

Não possui responsabilidades relacionadas a:

- regras de negócio;
- acesso ao banco de dados;
- manipulação de arquivos;
- geração de documentos.

---

# 16. Histórico

| Versão | Data       | Alteração                         |
| ------ | ---------- | --------------------------------- |
| 1.0    | 08/07/2026 | Primeira implementação do módulo. |
