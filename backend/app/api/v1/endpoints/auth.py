"""Authentication API endpoints."""

import random
import secrets
from typing import Any
from uuid import uuid4

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.redis import get_redis
from app.core.schemas import SuccessResponse
from app.models.user import User
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter()


class SendCodeRequest(BaseModel):
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)


class SendCodeResponse(BaseModel):
    code: str
    expires_in: int


class LoginWithCodeRequest(BaseModel):
    phone: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=255)
    code: str = Field(..., min_length=6, max_length=6)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict[str, Any]


def _get_identifier(email: str | None, phone: str | None) -> str:
    if not email and not phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone is required",
        )
    return email or phone


@router.post("/send-code")
async def send_code(
    request: SendCodeRequest,
    redis_client: redis.Redis = Depends(get_redis),
) -> SuccessResponse[SendCodeResponse]:
    identifier = _get_identifier(request.email, request.phone)
    
    # MVP: Generate simple code
    code = "".join(random.choices("0123456789", k=6))
    
    # Store in Redis
    key = f"auth:code:{identifier}"
    await redis_client.set(key, code, ex=300)

    return SuccessResponse(data=SendCodeResponse(
        code=code,
        expires_in=300,
    ))


@router.post("/login/code")
async def login_with_code(
    request: LoginWithCodeRequest,
    session: AsyncSession = Depends(get_session),
    redis_client: redis.Redis = Depends(get_redis),
    auth_service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[AuthTokens]:
    identifier = _get_identifier(request.email, request.phone)
    
    # Verify code
    key = f"auth:code:{identifier}"
    stored_code = await redis_client.get(key)
    
    if not stored_code or stored_code != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code",
        )
    
    await redis_client.delete(key)
    
    # Find or Create User
    stmt = select(User).where(
        or_(
            User.email == request.email if request.email else False,
            User.phone == request.phone if request.phone else False,
        )
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            id=str(uuid4()),
            email=request.email,
            phone=request.phone,
            password_hash="", # No password for code login
            is_active=True,
            nickname=f"User_{identifier[-4:]}"
        )
        session.add(user)
        await session.flush() # Ensure ID is generated
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    # Generate Tokens
    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(user.id)
    
    return SuccessResponse(data=AuthTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=auth_service.access_token_expire_minutes * 60,
        user={
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone
        }
    ))


@router.post("/token/refresh")
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> SuccessResponse[dict[str, Any]]:
    # Validate refresh token (simplified)
    try:
        payload = auth_service.decode_token(request.refresh_token)
        if payload.token_type != "refresh":
             raise HTTPException(status_code=401, detail="Invalid token type")
        
        new_access_token = auth_service.create_access_token(payload.user_id)
        return SuccessResponse(data={
            "access_token": new_access_token,
            "expires_in": auth_service.access_token_expire_minutes * 60
        })
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
