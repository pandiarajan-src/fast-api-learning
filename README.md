# Hello API (FastAPI)
Minimal FastAPI service used to bootstrap my portfolio.

## Quickstart
Without UV
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or use pip freeze from your env
uvicorn app.main:app --reload
```

With UV
```bash
uv sync
uv run pylint hello_world/main.py
uv run pre-commit run --all-files
uv run pytest -q --import-mode=importlib hello_world/tests/test_main.py
uv run uvicorn hello_world.main:app -reload 
```

## Endpoints
- `GET /` → `{"message": "Hello, FastAPI!"}`

## Docs
- Swagger UI: `/docs`
- ReDoc: `/redoc`
