"""Health check endpoint."""

from fastapi import APIRouter

from app.core.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    from app.core.config import settings

    return HealthResponse(status="healthy", version=settings.app_version)
