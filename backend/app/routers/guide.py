"""Agentic guidance endpoint."""

from fastapi import APIRouter

from app.models import GuideChatRequest, GuideChatResponse
from app.services.agent import guide_turn

router = APIRouter(prefix="/api/guide", tags=["guide"])


@router.post("/chat", response_model=GuideChatResponse)
async def chat(req: GuideChatRequest) -> GuideChatResponse:
    return await guide_turn(req)
