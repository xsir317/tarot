"""Tarot reading API endpoints."""

import random
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.schemas import SuccessResponse
from app.services.llm_service import LLMService
from app.data.tarot_cards import TAROT_CARDS


router = APIRouter()


class ValidateQuestionRequest(BaseModel):
    """Request model for question validation."""

    question: str
    gender: str
    language: str = "zh"


class DrawCardsRequest(BaseModel):
    """Request model for drawing cards."""

    device_fingerprint: str
    ip_address: str = "127.0.0.1"


class InterpretCardsRequest(BaseModel):
    """Request model for interpreting cards."""

    question: str
    gender: str
    language: str = "zh"
    cards: list[dict[str, Any]]


@router.post("/validate-question")
async def validate_question(
    request: ValidateQuestionRequest,
    llm_service: LLMService = Depends(lambda: LLMService()),
) -> SuccessResponse[dict[str, Any]]:
    """Validate if a question is suitable for tarot reading.

    This endpoint uses to LLM to determine if question is appropriate.
    """
    result = llm_service.validate_question_sync(
        request.question,
        request.gender,
        request.language,
    )

    return SuccessResponse(data={
        "suitable": result.suitable,
        "reason": result.reason,
        "redirect_message": result.redirect_message,
    })


@router.post("/draw-cards")
async def draw_cards(
    request: DrawCardsRequest,
) -> SuccessResponse[dict[str, Any]]:
    """Draw 3 random tarot cards.

    Each card can be either upright or reversed.
    """
    # Select 3 random cards without replacement
    selected_cards = random.sample(TAROT_CARDS, 3)

    # Determine position (upright or reversed) for each card
    cards = []
    for card in selected_cards:
        cards.append({
            "id": card["id"],
            "name": card["name"],
            "name_en": card["name_en"],
            "name_zh": card["name_zh"],
            "position": "upright" if random.choice([True, False]) else "reversed",
        })

    return SuccessResponse(data={"cards": cards})


@router.post("/interpret")
async def interpret_cards(
    request: InterpretCardsRequest,
    llm_service: LLMService = Depends(lambda: LLMService()),
) -> SuccessResponse[dict[str, Any]]:
    """Interpret drawn tarot cards.

    This endpoint uses to LLM to provide interpretations for the drawn cards.
    """
    result = llm_service.interpret_cards_sync(
        request.question,
        request.gender,
        request.cards,
        request.language,
    )

    return SuccessResponse(data={
        "interpretations": [
            {
                "card_index": interp.card_index,
                "card_name": interp.card_name,
                "position": interp.position,
                "interpretation": interp.interpretation,
            }
            for interp in result.interpretations
        ],
        "overall_interpretation": result.overall_interpretation,
    })
