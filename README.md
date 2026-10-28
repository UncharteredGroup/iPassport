# iPassport — AI-Powered Remote Passport Application & Identity Verification

> **Disclaimer:** iPassport is an independent civic-technology demonstration
> built for the Meta Global AI Developer Hackathon 2026. It is **not** an
> official service of the Government of Uganda, the Ministry of Internal
> Affairs, or the Directorate of Citizenship and Immigration Control (DCIC).
> No real passport is issued. All verification results are labelled AI-assisted.

iPassport shows how agentic AI and image recognition can collapse the Ugandan
passport journey — online form → bank payment → travel to a centre for
biometrics → queues and repeat visits — into one guided digital session with an
auditable, high-assurance application package.

## How it works

1. **Agentic guide** (Muse Spark): conversational agent asks only what the
   application type needs, explains every requirement, and blocks submission
   until evidence is complete.
2. **Document verification** (SAM 3.1): National ID, recommender ID, birth
   certificate, or old passport are segmented into regions (photo, name, NIN,
   dates), extracted, and cross-checked against user input.
3. **Biometric & liveness check**: guided selfie / short video, face match
   against ID photos, presentation-attack indicators, confidence scores.
4. **Passport photo validation**: ICAO-style checks (background, face size,
   lighting) with retake guidance.
5. **Packaging**: verified data + evidence + model scores + audit log are
   compiled into one signed JSON package with an overall risk score.
6. **Transparency**: every AI decision shows its evidence and confidence, with
   one-click escalation to a human-review queue.

## Repository layout

| Path | Contents |
|------|----------|
| `frontend/` | PWA (React + Vite + TypeScript), camera capture, guided steps |
| `backend/` | FastAPI service: agent, vision, photo, packaging, audit |
| `docs/` | Demo script, API reference, threat model, responsible-use notes |
| `.github/workflows/` | CI: frontend build + backend tests |

## Quick start (demo mode, no API keys)

Demo mode runs the full flow with a deterministic mock provider so the UI,
scoring, and packaging work without Meta Model API access.

```bash
# Backend (Python 3.11+)
cd backend
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

```bash
# Frontend (Node 20+)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in a browser. The app talks to
http://localhost:8000 by default (`VITE_API_BASE`).

## Live Meta Model API mode

Set these in `backend/.env` (see [.env.example](.env.example)):

```bash
IPASSPORT_MOCK_MODE=false
META_API_KEY=your-key
META_API_BASE=https://api.meta.com/v1
META_AGENT_MODEL=muse-spark
META_VISION_MODEL=sam-3.1
META_IMAGE_MODEL=muse-image
```

The provider layer (`backend/app/providers/`) isolates all model calls, so
swapping models or adding a national-system connector means changing one
module, not the flow logic.

## API overview

- `POST /api/guide/chat` — agentic guidance turn
- `POST /api/verify/document` — document segmentation + extraction + checks
- `POST /api/verify/face` — face match + liveness scoring
- `POST /api/verify/photo` — passport photo ICAO checks
- `POST /api/package` — build signed application package
- `GET /api/status/{package_id}` — tracker stages
- `POST /api/review/escalate` — send package to human review

Full reference: [docs/API.md](docs/API.md).

## Privacy & responsible use

- Evidence images are temporary (default 24 h retention) and deleted after
  packaging unless the user opts in.
- No training on user data without explicit consent.
- Every score ships with evidence and a human-override path.
- Threat model and misuse notes: [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues: Luganda
translations, photo-standards engine, mobile-money payment stub, offline
guidance.

## License

MIT — see [LICENSE](LICENSE).
