# First Python FastAPI 🚀
My first FastAPI project

## Run
```
pip3 install -r requirements.txt
fastapi dev main.py
```

## Virtual environment
Install deps:
```
pip3 install -r requirements.txt
```

Activate:
```
source .venv/bin/activate
```

Deactivate:
```
deactivate
```

## Deps
"fastapi[standard]"
pytest


## Test
```
pytest test_app.py
```

## Decisions
## Pydantic vs Dataclasses
pydantic: integrated to the api, robust validation, helps in doc generation
dataclasses: preferred for internal data structures, performatic, more work to validade

trade-off: Pydantic has a cost for its powerful data validation and parsing features

## Utils
[Guia Completo para Usar o Virtual Environment (venv) no Python](https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo)

[Virtual Environments](https://fastapi.tiangolo.com/virtual-environments/#check-the-virtual-environment-is-active)
