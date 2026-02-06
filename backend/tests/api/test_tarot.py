import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.services.llm_service import LLMService, ValidationResult, InterpretationResult, CardInterpretation, get_llm_service
from app.api.v1.endpoints.tarot import validate_question

# Mock Service
class MockLLMService:
    async def validate_question(self, question, gender, language):
        return ValidationResult(
            suitable=True,
            reason="Suitable",
            redirect_message=None
        )

    async def interpret_cards(self, question, gender, cards, language):
        return InterpretationResult(
            interpretations=[
                CardInterpretation(
                    card_index=i,
                    card_name=c["name"],
                    position=c["position"],
                    interpretation="Mock interpretation"
                ) for i, c in enumerate(cards)
            ],
            overall_interpretation="Overall mock interpretation"
        )

@pytest.fixture
def mock_llm_service():
    return MockLLMService()

@pytest.mark.asyncio
async def test_tarot_flow(client: TestClient, mock_llm_service):
    # Override Dependency
    from app.main import app
    app.dependency_overrides[get_llm_service] = lambda: mock_llm_service
    
    # 1. Validate Question
    response = client.post("/api/v1/tarot/validate", json={
        "question": "Is this a good time to start a business?",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["suitable"] is True

    # 2. Draw Cards
    response = client.post("/api/v1/tarot/draw", json={})
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["cards"]) == 3
    cards = data["cards"]
    
    # 3. Interpret
    response = client.post("/api/v1/tarot/interpret", json={
        "question": "Is this a good time to start a business?",
        "cards": [
            {"id": c["id"], "name": c["name"], "position": c["position"]} for c in cards
        ],
        "language": "en",
        "device_fingerprint": "test_fingerprint"
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "reading_id" in data
    assert len(data["interpretations"]) == 3
    assert "overall_interpretation" in data
    
    # Clear overrides
    app.dependency_overrides = {}
