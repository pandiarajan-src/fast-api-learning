# Hello API (FastAPI)
Minimal FastAPI service used to bootstrap my portfolio.

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or use pip freeze from your env
uvicorn app.main:app --reload
```

## Endpoints
- `GET /` → `{"message": "Hello, FastAPI!"}`

## Docs
- Swagger UI: `/docs`
- ReDoc: `/redoc`
