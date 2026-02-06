"""Tarot reading API endpoints."""

import random
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.schemas import SuccessResponse
from app.services.llm_service import LLMService, ValidationResult, InterpretationResult, get_llm_service
from app.data.tarot_cards import TAROT_CARDS

router = APIRouter()


class ValidateQuestionRequest(BaseModel):
    question: str
    gender: str | None = None
    language: str = "zh"


class DrawCardsResponse(BaseModel):
    cards: list[dict[str, Any]]


class InterpretCardsRequest(BaseModel):
    question: str
    cards: list[dict[str, Any]]
    language: str = "zh"
    device_fingerprint: str | None = None


class InterpretCardsResponse(BaseModel):
    reading_id: str
    interpretations: list[dict[str, Any]]
    overall_interpretation: str


@router.post("/validate")
async def validate_question(
    request: ValidateQuestionRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> SuccessResponse[dict[str, Any]]:
    # In production, we would use the async method.
    # For MVP without API Key, we might fallback to sync mock if key is missing,
    # or better, rely on the Test to mock the service.
    # Here I will call the async method, assuming the test will mock it.
    
    # NOTE: Since we are in "Red-Green" and I don't have an API Key in env,
    # running this manually would fail. But the test should mock it.
    # However, to be safe for manual testing (if needed), I will check if API key is set?
    # No, let's stick to standard dependency injection.
    
    result = await llm_service.validate_question(
        request.question,
        request.gender or "unknown",
        request.language,
    )

    return SuccessResponse(data={
        "suitable": result.suitable,
        "reason": result.reason,
        "redirect_message": result.redirect_message,
    })


@router.post("/draw")
async def draw_cards() -> SuccessResponse[DrawCardsResponse]:
    # Filter out empty entries if any (though we cleaned them up)
    valid_cards = [c for c in TAROT_CARDS if c["id"]]
    selected_cards = random.sample(valid_cards, 3)
    
    cards = []
    for card in selected_cards:
        cards.append({
            "id": card["id"],
            "name_key": card["name_key"],
            "image": card["image"],
            "position": "upright" if random.choice([True, False]) else "reversed",
        })

    return SuccessResponse(data=DrawCardsResponse(cards=cards))


@router.post("/interpret")
async def interpret_cards(
    request: InterpretCardsRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> SuccessResponse[InterpretCardsResponse]:
    result = await llm_service.interpret_cards(
        request.question,
        "unknown", # Gender not in request? Check API design. API design has gender in validate, but not interpret? 
                   # Design says: "Interpret" request body has "question", "cards", "language".
                   # It seems I missed "gender" in Interpret request in API Design, or it's stateless?
                   # Actually, usually we pass context. Let's add gender to request or default to unknown.
        request.cards,
        request.language,
    )
    
    # Mock saving reading to DB
    reading_id = str(uuid4())
    
    return SuccessResponse(data=InterpretCardsResponse(
        reading_id=reading_id,
        interpretations=[
            {
                "card_id": interp.card_name, # Map correctly based on LLM output
                "text": interp.interpretation,
                # "card_index": interp.card_index
            }
            for interp in result.interpretations
        ],
        overall_interpretation=result.overall_interpretation,
    ))
