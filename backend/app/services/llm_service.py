"""LLM service for question validation and tarot interpretation."""

from pathlib import Path
from typing import Any

import litellm
from jinja2 import Environment, FileSystemLoader
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
        
        # Initialize Jinja2 environment
        template_dir = Path(__file__).resolve().parent.parent / "templates" / "prompts"
        self._jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def _render_template(self, template_name: str, **kwargs: Any) -> str:
        """Render a Jinja2 template.

        Args:
            template_name: Name of the template file
            **kwargs: Context variables for the template

        Returns:
            Rendered string
        """
        template = self._jinja_env.get_template(template_name)
        return template.render(**kwargs)

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
            system_prompt = self._render_template("system.j2", language=language)
            user_prompt = self._render_template(
                "validation.j2",
                question=question,
                gender=gender,
            )

            response = await litellm.acompletion(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                api_key=self._api_key,
                response_format={"type": "json_object"},
            )

            # litellm returns a ModelResponse object, similar to OpenAI
            content = response.choices[0].message.content
            return ValidationResult.model_validate_json(content)

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
            system_prompt = self._render_template("system.j2", language=language)
            user_prompt = self._render_template(
                "interpretation.j2",
                question=question,
                gender=gender,
                cards=cards,
            )

            response = await litellm.acompletion(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                api_key=self._api_key,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            return InterpretationResult.model_validate_json(content)

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
