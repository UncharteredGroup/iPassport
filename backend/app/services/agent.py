"""Agentic guidance: one turn of the Muse-powered application guide."""

import uuid

from app.models import GuideChatRequest, GuideChatResponse
from app.providers import get_provider
from app.services.audit import audit


async def guide_turn(req: GuideChatRequest) -> GuideChatResponse:
    session_id = req.session_id or str(uuid.uuid4())
    provider = get_provider()
    result = await provider.agent_turn(
        req.application_type, [m.model_dump() for m in req.messages]
    )
    audit.record("guide_turn", session_id, {
        "provider": provider.name, "application_type": req.application_type,
        "missing": result.get("missing_fields", []),
    })
    return GuideChatResponse(
        session_id=session_id,
        reply=result.get("reply", ""),
        missing_fields=result.get("missing_fields", []),
        next_actions=result.get("next_actions", []),
        done=bool(result.get("done", False)),
    )
