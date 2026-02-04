"""Test authentication service."""

import pytest
from datetime import datetime, timedelta, timezone

from app.services.auth_service import AuthService, TokenPayload
from app.core.exceptions import AuthenticationError


def test_password_hashing():
    """Test password hashing and verification."""
    service = AuthService()
    password = "secure_password_123"

    hashed = service.hash_password(password)
    assert hashed != password
    assert len(hashed) > 50  # bcrypt hashes are long

    # Correct password
    assert service.verify_password(password, hashed) is True

    # Wrong password
    assert service.verify_password("wrong_password", hashed) is False


def test_access_token_creation():
    """Test creating access token."""
    service = AuthService()
    user_id = "test-user-id-123"

    token = service.create_access_token(user_id)
    assert isinstance(token, str)
    assert len(token) > 20


def test_refresh_token_creation():
    """Test creating refresh token."""
    service = AuthService()
    user_id = "test-user-id-123"

    token = service.create_refresh_token(user_id)
    assert isinstance(token, str)
    assert len(token) > 20


def test_token_decode_valid():
    """Test decoding a valid token."""
    service = AuthService()
    user_id = "test-user-id-123"

    token = service.create_access_token(user_id)
    payload = service.decode_token(token)

    assert payload.user_id == user_id
    assert payload.token_type == "access"


def test_token_decode_invalid():
    """Test decoding an invalid token raises exception."""
    service = AuthService()

    with pytest.raises(AuthenticationError, match="Invalid or expired token"):
        service.decode_token("invalid_token_string")


def test_token_decode_expired():
    """Test decoding an expired token raises exception."""
    service = AuthService()
    # Override access token expire time to -1 hour for testing
    original_expire = service.access_token_expire_minutes
    service.access_token_expire_minutes = -60

    user_id = "test-user-id-123"
    token = service.create_access_token(user_id)

    # Restore original expire time
    service.access_token_expire_minutes = original_expire

    with pytest.raises(AuthenticationError, match="Invalid or expired token"):
        service.decode_token(token)


def test_generate_device_fingerprint():
    """Test generating device fingerprint."""
    service = AuthService()
    fp = service.generate_device_fingerprint()

    assert isinstance(fp, str)
    assert len(fp) >= 32
