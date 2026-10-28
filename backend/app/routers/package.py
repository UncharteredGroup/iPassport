"""Packaging + status tracker endpoints."""

from fastapi import APIRouter

from app.models import PackageRequest, PackageResponse, StatusResponse
from app.services.packaging import build_package, get_status

router = APIRouter(prefix="/api", tags=["package"])


@router.post("/package", response_model=PackageResponse)
async def package(req: PackageRequest) -> PackageResponse:
    return await build_package(req)


@router.get("/status/{package_id}", response_model=StatusResponse)
async def status(package_id: str) -> StatusResponse:
    return await get_status(package_id)
