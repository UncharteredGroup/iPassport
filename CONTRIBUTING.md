# Contributing to iPassport

Thanks for helping build open, auditable identity tooling. A few ground rules:

## Setup

- Backend: Python 3.11+, `pip install -e ".[dev]"` from `backend/`.
- Frontend: Node 20+, `npm install` from `frontend/`.
- Copy `.env.example` to `backend/.env` for local settings. Never commit keys.

## Workflow

1. Fork and branch from `main` (`feat/…`, `fix/…`, `docs/…`).
2. Keep PRs small and scoped; one feature per PR.
3. Add or update tests for backend logic (`backend/tests/`).
4. Run checks before pushing:
   - `cd backend && ruff check . && pytest`
   - `cd frontend && npm run build`
5. Describe the user-visible change and any model-behaviour change in the PR.

## Identity-system responsibility

- Never weaken a verification check to make a demo pass; add explicit mock
  fixtures instead.
- New scores must ship with evidence references and a confidence value.
- Borderline cases must escalate to human review, not auto-pass.
- Do not add tracking, analytics, or data retention beyond the documented
  minimums without a reviewed proposal.

## Languages & accessibility

Luganda and other local-language contributions are welcome. Keep wording plain,
keep contrast high, and test flows on a small (360 px) viewport.
