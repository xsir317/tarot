"""Test LLM service."""

import pytest

from app.services.llm_service import LLMService
from app.core.exceptions import TarotError


def test_validate_question_suitable():
    """Test validating a suitable question."""
    service = LLMService()

    result = service.validate_question_sync(
        question="我最近工作不顺，不知道该怎么办？",
        gender="male",
        language="zh",
    )

    assert result.suitable is True
    assert len(result.reason) > 0
    assert result.redirect_message is None


def test_validate_question_unsuitable_pain():
    """Test validating an unsuitable question about pain."""
    service = LLMService()

    result = service.validate_question_sync(
        question="I feel painful, what should I do?",
        gender="female",
        language="zh",
    )

    assert result.suitable is False
    assert "medical" in result.redirect_message.lower() or "doctor" in result.redirect_message.lower()


def test_validate_question_unsuitable_factual():
    """Test validating an unsuitable factual question."""
    service = LLMService()

    result = service.validate_question_sync(
        question="Calculate the formula for gravity",
        gender="male",
        language="zh",
    )

    assert result.suitable is False
    assert "factual" in result.redirect_message.lower() or "search engine" in result.redirect_message.lower()


def test_interpret_cards():
    """Test interpreting tarot cards."""
    service = LLMService()

    result = service.interpret_cards_sync(
        question="我的爱情运势如何？",
        gender="female",
        language="zh",
        cards=[
            {"name": "愚者", "position": "upright"},
            {"name": "恋人", "position": "reversed"},
            {"name": "高塔", "position": "upright"},
        ],
    )

    assert len(result.interpretations) == 3
    for i, interp in enumerate(result.interpretations):
        assert interp.card_name is not None
        assert interp.interpretation is not None

    assert len(result.overall_interpretation) > 0
