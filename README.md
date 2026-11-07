# Histórico de Atendimentos

Sistema em Django que registra e analisa a participação de colaboradores em atendimentos operacionais.

Uma mesma demanda pode ter vários participantes. Cada participação é um registro próprio, então uma demanda compartilhada conta uma vez para cada pessoa.

## Modelo de dados

| Modelo | Responsabilidade |
| --- | --- |
| `Colaborador` | Pessoa que realiza atendimentos |
| `Demanda` | Um atendimento (tipo e data) |
| `Participacao` | Liga uma demanda a um colaborador; única por par (demanda, colaborador) |

`Equipe` fica fora desta fase e entra depois por migration.

## Consultas (`operacoes/selectors.py`)

Todas aceitam os filtros `ano`, `mes`, `data_ini`, `data_fim`, `tipo` e `colaborador_id`.

- `total_por_colaborador()`: total de atendimentos por pessoa
- `historico(colaborador_id)`: datas e tipos de um colaborador
- `por_tipo(colaborador_id)`: total por tipo de demanda
- `comparar(nomes)`: totais de um grupo de colaboradores

## Rodar localmente

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

## Rodar no Google Colab

Use o notebook `bootstrap_atendimentos.ipynb`. Ele clona este repositório, aponta o banco para o Google Drive e roda as migrations.

## Configuração por variáveis de ambiente

| Variável | Padrão | Uso |
| --- | --- | --- |
| `ATENDIMENTOS_DB` | `db.sqlite3` na raiz do projeto | Caminho do arquivo SQLite |
| `DJANGO_SECRET_KEY` | chave de desenvolvimento | Defina em qualquer ambiente real |
| `DJANGO_DEBUG` | `1` | Use `0` fora do desenvolvimento |

## Próximos passos

1. Admin do Django para cadastro por tela
2. Relatórios e gráficos
3. Interface com filtros
4. Equipes
5. PostgreSQL para uso real
