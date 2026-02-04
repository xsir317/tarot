"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    health,
    payment,
    tarot,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tarot.router, prefix="/tarot", tags=["tarot"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])
