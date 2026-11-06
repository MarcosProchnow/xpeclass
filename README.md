# xpeclass

Exemplo de MLOps em Python: uma API [Flask](https://flask.palletsprojects.com) com um único endpoint, protegido por token, que treina um `RandomForestClassifier` com o dataset Iris e devolve as métricas de avaliação.

O projeto é didático. Toda a lógica está em [`app.py`](app.py). A API treina e avalia, mas **não serve previsões**: o modelo é descartado ao fim de cada requisição.

## Endpoint

| Método | Rota | Autenticação | O que faz |
|---|---|---|---|
| `GET` | `/train` | Parâmetro `token` na URL | Treina o modelo (70/30) e retorna a acurácia e o `classification_report` do scikit-learn |

Sem token, ou com token inválido, a resposta é `401`.

Exemplo de chamada:

```bash
curl "http://127.0.0.1:5000/train?token=SEU_TOKEN"
```

Formato da resposta:

```json
{
  "accuracy": "<float>",
  "classification_report": {
    "setosa": {"precision": "<float>", "recall": "<float>", "f1-score": "<float>", "support": "<float>"},
    "versicolor": {},
    "virginica": {},
    "accuracy": "<float>",
    "macro avg": {},
    "weighted avg": {}
  }
}
```

## Como rodar

Requisitos: Python 3.11 ou superior, [Poetry](https://python-poetry.org) e internet na primeira execução, porque o dataset é baixado pelo seaborn.

```bash
poetry install --no-root
```

Crie um arquivo `.env` na raiz do projeto. Ele já está no `.gitignore`:

```bash
echo "VALID_TOKEN=123456" > .env
```

Use outro valor fora do ambiente local. Depois, suba a API:

```bash
poetry run python app.py
```

Ela abre em `http://127.0.0.1:5000`, em modo de depuração. O arquivo [`rest.http`](rest.http) traz a chamada de exemplo para a extensão REST Client do VS Code.

## Testes

```bash
poetry run pytest
```

O [`test_app.py`](test_app.py) define o próprio token, então os testes não precisam do `.env`. Eles cobrem o `401` sem token e com token inválido, além do formato da resposta de um treino autorizado.

## Estrutura

```text
.
├── app.py          # treino, avaliação e endpoint
├── test_app.py     # testes do endpoint
├── rest.http       # chamada de exemplo
└── pyproject.toml  # dependências (Poetry)
```

## Limitações conhecidas

- **Token na URL:** query strings costumam aparecer em logs de servidores e proxies. Em produção, o token deveria ir no cabeçalho `Authorization`.
- **Modo de depuração:** `app.py` inicia com `debug=True`, adequado só para uso local. O `gunicorn` está nas dependências para servir a aplicação fora desse modo.
- **Treino por `GET`:** cada chamada consome CPU e não há limite de requisições.
- **Sem persistência:** o modelo treinado não é salvo nem pode ser consultado depois.
- **Sem CI:** os testes só rodam manualmente.
- **Licença:** o `pyproject.toml` declara MIT, mas o repositório ainda não tem o arquivo `LICENSE`.
