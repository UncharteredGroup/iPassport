"""Packaging, status, and escalation tests."""

import asyncio

from app.models import Applicant, EscalateRequest, PackageRequest
from app.services.packaging import build_package, escalate, get_status


def _req() -> PackageRequest:
    return PackageRequest(
        session_id="test-session",
        applicant=Applicant(surname="DEMO", given_names="APPLICANT",
                            nin="CM123456X", dob="1990-01-01"),
        application_type="renewal",
        evidence={"document_ids": ["doc-1"], "face_id": "face-1", "photo_id": "ph-1"},
        payment_ref="demo-pay-001",
    )


def test_build_package_returns_signed_low_risk_for_full_evidence():
    resp = asyncio.run(build_package(_req()))
    assert resp.package_id
    assert resp.risk_score < 0.3
    assert resp.signature.startswith("hmac-sha256:")
    assert resp.summary["ai_assisted"] is True


def test_missing_evidence_raises_risk():
    req = _req()
    req.evidence = {}
    resp = asyncio.run(build_package(req))
    assert resp.risk_score >= 0.4


def test_status_tracks_package_stages():
    resp = asyncio.run(build_package(_req()))
    status = asyncio.run(get_status(resp.package_id))
    assert status.stage == "ai_verified"
    assert [h.stage for h in status.history] == ["captured", "ai_verified"]


def test_unknown_package_reports_unknown():
    status = asyncio.run(get_status("no-such-id"))
    assert status.stage == "unknown"


def test_escalate_queues_for_review():
    resp = asyncio.run(build_package(_req()))
    out = asyncio.run(escalate(EscalateRequest(
        package_id=resp.package_id, reason="demo check")))
    assert out.queued is True
    assert out.position >= 1
