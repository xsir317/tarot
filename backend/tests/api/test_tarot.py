"""Test tarot API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_validate_question_endpoint():
    """Test question validation endpoint."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/tarot/validate-question",
        json={
            "question": "I am confused about my work, what should I do?",
            "gender": "male",
            "language": "en",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["suitable"] is True


def test_validate_question_endpoint_unsuitable():
    """Test question validation endpoint for unsuitable question."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/tarot/validate-question",
        json={
            "question": "I feel painful, what should I do?",
            "gender": "female",
            "language": "en",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["suitable"] is False
    assert data["data"]["redirect_message"] is not None


def test_draw_cards_endpoint():
    """Test draw cards endpoint."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/tarot/draw-cards",
        json={
            "device_fingerprint": "test-device-123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    cards = data["data"]["cards"]
    assert len(cards) == 3

    # Check card structure
    for card in cards:
        assert "id" in card
        assert "name" in card
        assert "position" in card
        assert card["position"] in ["upright", "reversed"]


def test_interpret_cards_endpoint():
    """Test interpret cards endpoint."""
    client = TestClient(app)

    response = client.post(
        "/api/v1/tarot/interpret",
        json={
            "question": "How is my love life?",
            "gender": "female",
            "language": "en",
            "cards": [
                {"id": "0", "position": "upright"},
                {"id": "6", "position": "reversed"},
                {"id": "16", "position": "upright"},
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    result = data["data"]
    assert "interpretations" in result
    assert "overall_interpretation" in result
    assert len(result["interpretations"]) == 3
