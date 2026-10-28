"""Verification decision tests (mock provider, no network)."""

import asyncio

from app.models import (
    DocumentVerifyRequest,
    FaceVerifyRequest,
    PhotoVerifyRequest,
)
from app.services.photo import assess_photo
from app.services.vision import verify_document, verify_face

BIG_IMAGE = "data:image/jpeg;base64," + "A" * 2000
TINY_IMAGE = "data:image/jpeg;base64,AAA"


def test_document_accepts_clean_capture_with_matching_nin():
    # Mock extracts a deterministic NIN; compute it first, then expect a match.
    first = asyncio.run(verify_document(DocumentVerifyRequest(
        document_type="national_id_front", image=BIG_IMAGE)))
    req = DocumentVerifyRequest(
        document_type="national_id_front", image=BIG_IMAGE,
        expected={"nin": first.extracted["nin"]},
    )
    resp = asyncio.run(verify_document(req))
    assert resp.decision == "accept"
    assert resp.quality_score >= 0.6
    assert any(r.label == "nin" for r in resp.regions)


def test_document_requests_retake_for_tiny_image():
    resp = asyncio.run(verify_document(DocumentVerifyRequest(
        document_type="national_id_front", image=TINY_IMAGE)))
    assert resp.decision == "retake"
    assert resp.quality_issues


def test_document_escalates_on_field_mismatch():
    resp = asyncio.run(verify_document(DocumentVerifyRequest(
        document_type="national_id_front", image=BIG_IMAGE,
        expected={"nin": "CM000000Z"},
    )))
    assert resp.decision == "escalate"


def test_face_accepts_with_liveness_events():
    resp = asyncio.run(verify_face(FaceVerifyRequest(
        selfie=BIG_IMAGE, references=[BIG_IMAGE],
        liveness_events=[{"prompt": "blink", "passed": True}],
    )))
    assert resp.decision == "accept"
    assert resp.liveness_score >= 0.7


def test_face_escalates_without_liveness():
    resp = asyncio.run(verify_face(FaceVerifyRequest(
        selfie=BIG_IMAGE, references=[BIG_IMAGE], liveness_events=[])))
    assert resp.decision == "escalate"


def test_photo_accepts_clean_capture():
    resp = asyncio.run(assess_photo(PhotoVerifyRequest(image=BIG_IMAGE)))
    assert resp.decision == "accept"
    assert all(c.passed for c in resp.icao_checks)


def test_photo_requests_retake_for_tiny_image():
    resp = asyncio.run(assess_photo(PhotoVerifyRequest(image=TINY_IMAGE)))
    assert resp.decision == "retake"
