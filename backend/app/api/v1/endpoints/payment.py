"""Payment endpoints."""

from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.schemas import SuccessResponse

router = APIRouter()


class CheckoutSessionRequest(BaseModel):
    product_type: str  # subscription / one_time / tip
    price_id: str | None = None
    amount: int | None = None
    currency: str = "usd"
    reading_id: str | None = None
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    checkout_url: str


@router.post("/checkout")
async def create_checkout_session(
    request: CheckoutSessionRequest,
) -> SuccessResponse[CheckoutSessionResponse]:
    """Create a Stripe checkout session."""
    # TODO: Implement Stripe integration
    # Logic:
    # 1. If product_type == "subscription", use price_id
    # 2. If product_type == "tip", use amount + currency + reading_id metadata
    
    # Mock response
    return SuccessResponse(data=CheckoutSessionResponse(
        checkout_url="https://checkout.stripe.com/test/mock"
    ))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Stripe webhook handler."""
    return {"status": "success"}
