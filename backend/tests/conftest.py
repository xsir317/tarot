"""Pytest configuration and fixtures."""

import pytest
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.redis import get_redis
from app.core.database import get_session

class MockRedis:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value
        return True

    async def delete(self, key):
        if key in self.store:
            del self.store[key]
        return True

@pytest.fixture
def mock_redis():
    return MockRedis()

@pytest.fixture
def client(mock_redis) -> Generator[TestClient, None, None]:
    """Create test client."""
    # Override Redis dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    
    # Override DB Session
    async def override_get_session():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides = {}

@pytest.fixture
def anyio_backend() -> str:
    """AnyIO backend for async tests."""
    return "asyncio"
