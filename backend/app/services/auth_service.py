"""Authentication service for password hashing and JWT tokens."""

import secrets
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import AuthenticationError


class TokenPayload(BaseModel):
    """JWT token payload."""

    user_id: str
    token_type: str
    exp: int
    iat: int


class AuthService:
    """Service for authentication operations."""

    def __init__(
        self,
        secret_key: str | None = None,
        access_token_expire_minutes: int | None = None,
        refresh_token_expire_days: int | None = None,
        bcrypt_rounds: int | None = None,
    ) -> None:
        """Initialize AuthService.

        Args:
            secret_key: JWT secret key (default from settings)
            access_token_expire_minutes: Access token expiration in minutes
            refresh_token_expire_days: Refresh token expiration in days
            bcrypt_rounds: Bcrypt hash rounds
        """
        self._secret_key = secret_key or settings.jwt_secret_key
        self._access_token_expire_minutes = access_token_expire_minutes or settings.access_token_expire_minutes
        self._refresh_token_expire_days = refresh_token_expire_days or settings.refresh_token_expire_days
        self._bcrypt_rounds = bcrypt_rounds or settings.bcrypt_rounds
        self._algorithm = settings.jwt_algorithm

    @property
    def access_token_expire_minutes(self) -> int:
        """Get access token expiration minutes."""
        return self._access_token_expire_minutes

    @access_token_expire_minutes.setter
    def access_token_expire_minutes(self, value: int) -> None:
        """Set access token expiration minutes."""
        self._access_token_expire_minutes = value

    @property
    def refresh_token_expire_days(self) -> int:
        """Get refresh token expiration days."""
        return self._refresh_token_expire_days

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt(rounds=self._bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hash.

        Args:
            password: Plain text password
            hashed_password: Bcrypt hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except (ValueError, TypeError):
            return False

    def create_access_token(self, user_id: str) -> str:
        """Create a JWT access token.

        Args:
            user_id: User ID to embed in token

        Returns:
            JWT access token string
        """
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=self._access_token_expire_minutes)

        payload: dict[str, Any] = {
            "user_id": user_id,
            "token_type": "access",
            "exp": exp.timestamp(),
            "iat": now.timestamp(),
        }

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create a JWT refresh token.

        Args:
            user_id: User ID to embed in token

        Returns:
            JWT refresh token string
        """
        now = datetime.now(timezone.utc)
        exp = now + timedelta(days=self._refresh_token_expire_days)

        payload: dict[str, Any] = {
            "user_id": user_id,
            "token_type": "refresh",
            "exp": exp.timestamp(),
            "iat": now.timestamp(),
        }

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        """Decode and validate a JWT token.

        Args:
            token: JWT token string

        Returns:
            TokenPayload with decoded data

        Raises:
            AuthenticationError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
            # Convert float timestamps to int for pydantic
            if "exp" in payload:
                payload["exp"] = int(payload["exp"])
            if "iat" in payload:
                payload["iat"] = int(payload["iat"])
            return TokenPayload.model_validate(payload)
        except JWTError as e:
            raise AuthenticationError(
                message="Invalid or expired token",
                details={"error": str(e)},
            ) from e

    def generate_device_fingerprint(self) -> str:
        """Generate a secure random device fingerprint.

        Returns:
            Random string suitable as device fingerprint
        """
        return secrets.token_urlsafe(32)


def get_auth_service() -> AuthService:
    """Get a configured AuthService instance."""
    return AuthService()
