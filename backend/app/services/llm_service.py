"""LLM service for question validation and tarot interpretation."""

from typing import Any

import openai
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import TarotError


class ValidationResult(BaseModel):
    """Result of question validation."""

    suitable: bool
    reason: str
    redirect_message: str | None = None


class CardInterpretation(BaseModel):
    """Interpretation of a single tarot card."""

    card_index: int
    card_name: str
    position: str
    interpretation: str


class InterpretationResult(BaseModel):
    """Result of tarot interpretation."""

    interpretations: list[CardInterpretation]
    overall_interpretation: str


class LLMService:
    """Service for LLM integration."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize LLMService.

        Args:
            api_key: OpenAI API key (default from settings)
            model: Model name (default from settings)
        """
        self._api_key = api_key or settings.openai_api_key
        self._model = model or settings.openai_model
        self._client = None

    def _get_client(self) -> openai.AsyncOpenAI:
        """Get OpenAI client (lazy initialization)."""
        if self._client is None:
            self._client = openai.AsyncOpenAI(api_key=self._api_key)
        return self._client

    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt with language specification.

        Args:
            language: User's preferred language (zh/ja/en)

        Returns:
            System prompt string
        """
        return f"""You must respond in {language} for all text responses."""

    def _build_validation_prompt(
        self,
        question: str,
        gender: str,
        language: str,
    ) -> str:
        """Build user prompt for question validation.

        Args:
            question: User's question
            gender: User's gender
            language: User's preferred language

        Returns:
            User prompt string
        """
        return f"""You are a responsible tarot reading assistant. Determine if user's question is suitable for tarot interpretation.

User's gender: {gender}
User's question: {question}

Return a JSON result:
{{
  "suitable": true/false,
  "reason": "Your judgment reason",
  "redirect_message": "If not suitable, give user guidance"
}}

Judgment criteria:
1. Prohibited questions: pain, injury, self-harm -> guide to professional help
2. Unsuitable questions: academic, factual queries -> guide to appropriate channels
3. Suitable questions: life confusion, relationships, career, spiritual matters"""

    def _build_interpretation_prompt(
        self,
        question: str,
        gender: str,
        cards: list[dict[str, Any]],
        language: str,
    ) -> str:
        """Build user prompt for tarot interpretation.

        Args:
            question: User's question
            gender: User's gender
            cards: List of drawn tarot cards
            language: User's preferred language (zh/ja/en)

        Returns:
            User prompt string
        """
        cards_text = "\n".join(
            f"{i+1}. {card.get('name', '')} ({card.get('position', '')})"
            for i, card in enumerate(cards)
        )

        return f"""You are an experienced tarot reader. Interpret three tarot cards.

User's gender: {gender}
User's question: {question}

Tarot cards:
{cards_text}

Requirements:
- Gentle, respectful tone; avoid absolute assertions
- 200-300 words total
- End with encouragement
- Return JSON format:
{{
  "interpretations": [
    {{
      "card_index": 0,
      "card_name": "card name",
      "position": "position",
      "interpretation": "interpretation text"
    }}
  ],
  "overall_interpretation": "overall interpretation"
}}

Tarot is guidance, not fate. Convey warmth and positivity."""

    async def validate_question(
        self,
        question: str,
        gender: str,
        language: str = "en",
    ) -> ValidationResult:
        """Validate if question is suitable for tarot reading.

        Args:
            question: User's question
            gender: User's gender
            language: User's preferred language (zh/ja/en)

        Returns:
            ValidationResult with validation result

        Raises:
            TarotError: If LLM call fails
        """
        try:
            client = self._get_client()

            response = await client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": self._build_system_prompt(language),
                    },
                    {
                        "role": "user",
                        "content": self._build_validation_prompt(
                            question, gender, language
                        ),
                    },
                ],
                response_format={"type": "json_object"},
            )

            return ValidationResult.model_validate(
                response.choices[0].message.content
            )

        except Exception as e:
            raise TarotError(
                message="Failed to validate question",
                details={"error": str(e)},
            ) from e

    def validate_question_sync(
        self,
        question: str,
        gender: str,
        language: str = "en",
    ) -> ValidationResult:
        """Synchronous wrapper for question validation (for testing).

        This is a simplified version that returns a mock result.
        Use async version for production.
        """
        # Simplified logic for testing without real LLM calls
        # In production, this should call async version in an async context
        pain_keywords = ["pain", "painful", "hurt", "injured", "injury", "self-harm", "suicide"]
        factual_keywords = ["calculate", "math", "equals", "formula", "science"]

        question_lower = question.lower()

        for keyword in pain_keywords:
            if keyword in question_lower:
                return ValidationResult(
                    suitable=False,
                    reason="This question concerns physical pain or mental health.",
                    redirect_message="Please consult with a doctor or mental health professional.",
                )

        for keyword in factual_keywords:
            if keyword in question_lower:
                return ValidationResult(
                    suitable=False,
                    reason="This question appears to be a factual query.",
                    redirect_message="Please use a search engine or calculator for factual questions.",
                )

        return ValidationResult(
            suitable=True,
            reason="This question is suitable for tarot reading.",
            redirect_message=None,
        )

    async def interpret_cards(
        self,
        question: str,
        gender: str,
        cards: list[dict[str, Any]],
        language: str = "en",
    ) -> InterpretationResult:
        """Interpret drawn tarot cards.

        Args:
            question: User's question
            gender: User's gender
            cards: List of drawn tarot cards
            language: User's preferred language (zh/ja/en)

        Returns:
            InterpretationResult with card interpretations

        Raises:
            TarotError: If LLM call fails
        """
        try:
            client = self._get_client()

            response = await client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": self._build_system_prompt(language),
                    },
                    {
                        "role": "user",
                        "content": self._build_interpretation_prompt(
                            question, gender, cards, language
                        ),
                    },
                ],
                response_format={"type": "json_object"},
            )

            return InterpretationResult.model_validate(
                response.choices[0].message.content
            )

        except Exception as e:
            raise TarotError(
                message="Failed to interpret cards",
                details={"error": str(e)},
            ) from e

    def interpret_cards_sync(
        self,
        question: str,
        gender: str,
        cards: list[dict[str, Any]],
        language: str = "en",
    ) -> InterpretationResult:
        """Synchronous wrapper for card interpretation (for testing).

        This is a simplified version that returns mock results.
        Use async version for production.
        """
        interpretations = []
        for i, card in enumerate(cards):
            card_name = card.get("name", "Unknown")
            position = card.get("position", "upright")
            interpretations.append(
                CardInterpretation(
                    card_index=i,
                    card_name=card_name,
                    position=position,
                    interpretation=f"({card_name}) represents new possibilities and guidance.",
                )
            )

        overall = (
            "These cards suggest a path forward. Trust in guidance you receive "
"and take action aligned with your true intentions."
        )

        return InterpretationResult(
            interpretations=interpretations,
            overall_interpretation=overall,
        )


def get_llm_service() -> LLMService:
    """Get a configured LLMService instance."""
    return LLMService()
