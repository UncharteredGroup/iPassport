"""Application packaging: signed JSON + tracker stages + review queue."""

import hashlib
import hmac
import json
from datetime import UTC, datetime

from app.config import get_settings
from app.models import (
    EscalateRequest,
    EscalateResponse,
    PackageRequest,
    PackageResponse,
    StatusEvent,
    StatusResponse,
    new_id,
)
from app.services.audit import audit

STAGES = ["captured", "ai_verified", "ready_for_official_review", "approved_for_issuance"]

_packages: dict[str, dict] = {}
_review_queue: list[dict] = []


def _sign(payload: str) -> str:
    key = get_settings().package_signing_key.encode()
    return "hmac-sha256:" + hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()


async def build_package(req: PackageRequest) -> PackageResponse:
    package_id = new_id()
    evidence = req.evidence or {}
    # Risk rises with each missing evidence ref; demo scoring, documented.
    provided = sum(1 for v in evidence.values() if v)
    risk = round(max(0.0, min(1.0, 0.45 - 0.1 * provided)), 3)
    summary = {
        "applicant": req.applicant.model_dump(),
        "application_type": req.application_type,
        "payment_ref": req.payment_ref,
        "evidence": evidence,
        "ai_assisted": True,
        "disclaimer": "Demonstration package. Not an official issuance.",
    }
    signature = _sign(json.dumps(summary, sort_keys=True))
    now = datetime.now(UTC)
    _packages[package_id] = {
        "summary": summary, "risk": risk, "signature": signature,
        "history": [StatusEvent(stage="captured", at=now),
                    StatusEvent(stage="ai_verified", at=now)],
    }
    audit_ref = audit.record("package", package_id, {"risk": risk, "evidence": evidence})
    return PackageResponse(package_id=package_id, risk_score=risk,
                           summary=summary, signature=signature, audit_ref=audit_ref)


async def get_status(package_id: str) -> StatusResponse:
    pkg = _packages.get(package_id)
    if pkg is None:
        return StatusResponse(package_id=package_id, stage="unknown", history=[])
    history = pkg["history"]
    return StatusResponse(package_id=package_id, stage=history[-1].stage, history=history)


async def escalate(req: EscalateRequest) -> EscalateResponse:
    _review_queue.append({"package_id": req.package_id, "reason": req.reason,
                          "at": datetime.now(UTC).isoformat()})
    audit.record("escalate", req.package_id, {"reason": req.reason})
    return EscalateResponse(package_id=req.package_id, queued=True,
                            position=len(_review_queue))
