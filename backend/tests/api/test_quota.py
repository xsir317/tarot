import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_quota_anonymous(client: TestClient):
    response = client.get("/api/v1/quota?device_fingerprint=test_device_123")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["type"] == "anonymous"
    assert "remaining" in data
    assert "total" in data
