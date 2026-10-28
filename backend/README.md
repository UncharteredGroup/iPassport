# iPassport backend

FastAPI service that orchestrates Meta Model API calls (Muse agent, SAM 3.1
vision, Muse Image photo checks), stores temporary evidence, and builds signed
application packages with an audit trail.

## Run

```bash
python -m venv .venv
.venv/Scripts/activate  # Windows (`source .venv/bin/activate` on macOS/Linux)
pip install -e ".[dev]"
cp ../.env.example .env  # adjust as needed
uvicorn app.main:app --reload --port 8000
```

Mock mode (`IPASSPORT_MOCK_MODE=true`, the default) runs every endpoint without
API keys using `app/providers/mock.py`. Set it to `false` and provide
`META_API_KEY` for live model calls via `app/providers/meta_api.py`.

## Checks

```bash
ruff check .
pytest
```
