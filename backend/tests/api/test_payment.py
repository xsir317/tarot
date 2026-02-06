import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_payment_checkout(client: TestClient):
    # Test Tip Creation
    response = client.post("/api/v1/payment/checkout", json={
        "product_type": "tip",
        "amount": 500,
        "currency": "usd",
        "reading_id": "test_reading_uuid",
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel"
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "checkout_url" in data
