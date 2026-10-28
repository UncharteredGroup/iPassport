"""Passport-photo ICAO-style assessment."""

from app.models import Check, PhotoVerifyRequest, PhotoVerifyResponse, new_id
from app.providers import get_provider
from app.services.audit import audit

PHOTO_THRESHOLD = 0.75


async def assess_photo(req: PhotoVerifyRequest) -> PhotoVerifyResponse:
    provider = get_provider()
    result = await provider.photo_assessment(req.image)
    evidence_id = new_id()
    score = float(result.get("score", 0.0))
    checks = [Check(**c) for c in result.get("checks", [])]
    if score < 0.5:
        decision = "retake"
    elif score >= PHOTO_THRESHOLD and all(c.passed for c in checks):
        decision = "accept"
    else:
        decision = "escalate"
    audit.record("verify_photo", evidence_id, {
        "provider": provider.name, "score": score,
        "checks": [c.model_dump() for c in checks], "decision": decision,
    })
    return PhotoVerifyResponse(
        evidence_id=evidence_id, icao_checks=checks, score=score,
        guidance=result.get("guidance", ""), decision=decision,
    )
