"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import guide_router, package_router, review_router, verify_router

settings = get_settings()

app = FastAPI(title="iPassport API", version="0.1.0",
              description="AI-assisted passport application verification (demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(guide_router)
app.include_router(verify_router)
app.include_router(package_router)
app.include_router(review_router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "mode": "mock" if settings.mock_mode else "live"}
