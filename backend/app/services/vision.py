"""Document + face verification with explainable decisions."""

from app.models import (
    Check,
    DocumentVerifyRequest,
    DocumentVerifyResponse,
    FaceVerifyRequest,
    FaceVerifyResponse,
    Region,
    new_id,
)
from app.providers import get_provider
from app.services.audit import audit

MATCH_THRESHOLD = 0.8
LIVENESS_THRESHOLD = 0.7
QUALITY_THRESHOLD = 0.6


async def verify_document(req: DocumentVerifyRequest) -> DocumentVerifyResponse:
    provider = get_provider()
    result = await provider.segment_document(req.document_type, req.image)
    evidence_id = new_id()
    quality = result.get("quality", {})
    extracted = result.get("extracted", {})

    checks: list[Check] = []
    for field, want in req.expected.items():
        got = extracted.get(field, "")
        checks.append(Check(
            name=f"{field}_match", passed=bool(got) and got == want,
            detail=f"expected={want!r} extracted={got!r}",
        ))
    quality_score = float(quality.get("score", 0.0))
    checks.append(Check(name="image_quality", passed=quality_score >= QUALITY_THRESHOLD,
                        detail=f"score={quality_score:.2f}"))

    if quality_score < QUALITY_THRESHOLD:
        decision = "retake"
    elif all(c.passed for c in checks):
        decision = "accept"
    else:
        decision = "escalate"

    audit.record("verify_document", evidence_id, {
        "provider": provider.name, "document_type": req.document_type,
        "checks": [c.model_dump() for c in checks], "decision": decision,
    })
    return DocumentVerifyResponse(
        evidence_id=evidence_id, extracted=extracted,
        regions=[Region(**r) for r in result.get("regions", [])],
        checks=checks, quality_score=quality_score,
        quality_issues=list(quality.get("issues", [])), decision=decision,
    )


async def verify_face(req: FaceVerifyRequest) -> FaceVerifyResponse:
    provider = get_provider()
    result = await provider.face_scores(
        req.selfie, req.references, [e.model_dump() for e in req.liveness_events]
    )
    evidence_id = new_id()
    match = float(result.get("match_score", 0.0))
    liveness = float(result.get("liveness_score", 0.0))
    if match < 0.5 or liveness < 0.4:
        decision = "retake"
    elif match >= MATCH_THRESHOLD and liveness >= LIVENESS_THRESHOLD:
        decision = "accept"
    else:
        decision = "escalate"
    audit.record("verify_face", evidence_id, {
        "provider": provider.name, "match": match, "liveness": liveness,
        "indicators": result.get("indicators", []), "decision": decision,
    })
    return FaceVerifyResponse(
        evidence_id=evidence_id, match_score=match, liveness_score=liveness,
        indicators=list(result.get("indicators", [])), decision=decision,
    )
