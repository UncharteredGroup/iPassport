"""Document, face, and photo verification endpoints."""

from fastapi import APIRouter

from app.models import (
    DocumentVerifyRequest,
    DocumentVerifyResponse,
    FaceVerifyRequest,
    FaceVerifyResponse,
    PhotoVerifyRequest,
    PhotoVerifyResponse,
)
from app.services.photo import assess_photo
from app.services.vision import verify_document, verify_face

router = APIRouter(prefix="/api/verify", tags=["verify"])


@router.post("/document", response_model=DocumentVerifyResponse)
async def document(req: DocumentVerifyRequest) -> DocumentVerifyResponse:
    return await verify_document(req)


@router.post("/face", response_model=FaceVerifyResponse)
async def face(req: FaceVerifyRequest) -> FaceVerifyResponse:
    return await verify_face(req)


@router.post("/photo", response_model=PhotoVerifyResponse)
async def photo(req: PhotoVerifyRequest) -> PhotoVerifyResponse:
    return await assess_photo(req)
