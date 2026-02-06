import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_auth_flow(client: TestClient):
    # 1. Send Verification Code
    response = client.post("/api/v1/auth/send-code", json={
        "phone": "+1234567890"
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "code" in data
    code = data["code"]
    
    # 2. Login with Code
    response = client.post("/api/v1/auth/login/code", json={
        "phone": "+1234567890",
        "code": code
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    refresh_token = data["refresh_token"]

    # 3. Refresh Token
    response = client.post("/api/v1/auth/token/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert "access_token" in data
