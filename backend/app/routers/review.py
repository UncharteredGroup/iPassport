"""Human-review escalation endpoint."""

from fastapi import APIRouter

from app.models import EscalateRequest, EscalateResponse
from app.services.packaging import escalate

router = APIRouter(prefix="/api/review", tags=["review"])


@router.post("/escalate", response_model=EscalateResponse)
async def escalate_to_human(req: EscalateRequest) -> EscalateResponse:
    return await escalate(req)
