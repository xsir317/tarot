"""Authentication API endpoints (fake implementation for testing)."""

import random
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

from app.core.schemas import SuccessResponse
from app.services.auth_service import AuthService, get_auth_service


router = APIRouter()
auth_service = get_auth_service()

# In-memory store for verification codes (testing only)
# In production, this would use email/SMS delivery
_verification_codes: dict[str, tuple[str, float]] = {}
_users: dict[str, dict[str, Any]] = {}  # user_id -> user data
_refresh_tokens: dict[str, str] = {}  # refresh_token -> user_id


class SendCodeRequest(BaseModel):
    """Request model for sending verification code."""

    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)


class SendCodeResponse(BaseModel):
    """Response model for sending verification code."""

    code: str
    expires_in: int


class VerifyCodeRequest(BaseModel):
    """Request model for verifying code."""

    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)
    code: str = Field(..., min_length=6, max_length=6)


class RegisterRequest(BaseModel):
    """Request model for user registration."""

    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=100)
    nickname: str | None = Field(None, max_length=100)
    gender: str | None = Field(None, max_length=20)


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=100)


class AuthTokens(BaseModel):
    """Authentication tokens."""

    access_token: str
    refresh_token: str


class AuthData(BaseModel):
    """User auth data."""

    user_id: str
    email: str | None = None
    phone: str | None = None
    nickname: str | None = None


@router.post("/send-code")
async def send_code(request: SendCodeRequest) -> SuccessResponse[SendCodeResponse]:
    """Send verification code (fake implementation).

    For testing purposes, this endpoint generates a random code
    and returns it to the client without sending real SMS/email.

    The client can directly use this code for verification.
    """
    # Validate at least one contact method is provided
    if not request.email and not request.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required",
        )

    # Use email or phone as identifier
    identifier = request.email or request.phone

    # Generate a random 6-digit code
    code = "".join(random.choices.digits, k=6))

    # Store the code with expiration (5 minutes = 300 seconds)
    _verification_codes[identifier] = (code, 300.0)

    return SuccessResponse(data=SendCodeResponse(
        code=code,
        expires_in=300,
    ))


@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest) -> SuccessResponse[dict]:
    """Verify a verification code."""

    # Validate at least one contact method is provided
    if not request.email and not request.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required",
        )

    # Use email or phone as identifier
    identifier = request.email or request.phone

    # Check if code exists and is not expired
    if identifier not in _verification_codes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No verification code found for this contact. Please send a new code.",
        )

    stored_code, expires_in = _verification_codes[identifier]

    # Check if code matches
    if stored_code != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )

    # Code is valid, remove it
    del _verification_codes[identifier]

    return SuccessResponse(data={"verified": True})


@router.post("/register")
async def register(request: RegisterRequest) -> SuccessResponse[AuthData]:
    """Register a new user (fake implementation)."""

    # Validate at least one contact method is provided
    if not request.email and not request.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required",
        )

    # Check if user already exists
    identifier = request.email or request.phone
    if identifier in _users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered",
        )

    # Hash password
    password_hash = auth_service.hash_password(request.password)

    # Generate user ID
    user_id = str(uuid4())

    # Create user
    _users[user_id] = {
        "email": request.email,
        "phone": request.phone,
        "password_hash": password_hash,
        "nickname": request.nickname,
        "gender": request.gender,
        "is_active": True,
    }

    return SuccessResponse(data=AuthData(
        user_id=user_id,
        email=request.email,
        phone=request.phone,
        nickname=request.nickname,
    ))


@router.post("/login")
async def login(request: LoginRequest) -> SuccessResponse[AuthTokens]:
    """Login user (fake implementation)."""

    # Validate at least one contact method is provided
    if not request.email and not request.phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required",
        )

    # Find user by email or phone
    identifier = request.email or request.phone
    user_id = None

    for uid, user_data in _users.items():
        if user_data.get("email") == identifier or user_data.get("phone") == identifier:
            user_id = uid
            break

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user_data = _users[user_id]

    # Verify password
    if not auth_service.verify_password(request.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Check if user is active
    if not user_data.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Generate tokens
    access_token = auth_service.create_access_token(user_id)
    refresh_token = auth_service.create_refresh_token(user_id)

    # Store refresh token
    _refresh_tokens[refresh_token] = user_id

    return SuccessResponse(data=AuthTokens(
        access_token=access_token,
        refresh_token=refresh_token,
    ))


@router.post("/logout")
async def logout() -> SuccessResponse[dict]:
    """Logout user (fake implementation)."""

    # In a real implementation, this would invalidate refresh token
    # For now, we just return success
    return SuccessResponse(data={"logged_out": True})


@router.post("/refresh")
async def refresh_token() -> SuccessResponse[AuthTokens]:
    """Refresh access token (fake implementation)."""

    # In a real implementation, this would:
    # 1. Extract refresh token from HTTP-only cookie
    # 2. Validate refresh token
    # 3. Generate new access token
    # 4. Return new tokens

    # For testing, we return mock success
    return SuccessResponse(data=AuthTokens(
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
    ))


def get_verification_code(identifier: str) -> tuple[str, float] | None:
    """Get verification code and expiry (for internal use)."""
    return _verification_codes.get(identifier)


def get_user(user_id: str) -> dict[str, Any] | None:
    """Get user data (for internal use)."""
    return _users.get(user_id)


def validate_refresh_token(refresh_token: str) -> str | None:
    """Validate refresh token and return user_id (for internal use)."""
    return _refresh_tokens.get(refresh_token)


def invalidate_refresh_token(refresh_token: str) -> None:
    """Invalidate a refresh token (for internal use)."""
    if refresh_token in _refresh_tokens:
        del _refresh_tokens[refresh_token]


def clear_auth_store() -> None:
    """Clear all auth data (for testing only)."""
    global _verification_codes, _users, _refresh_tokens
    _verification_codes.clear()
    _users.clear()
    _refresh_tokens.clear()
