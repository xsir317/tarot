"""Quota management service."""

from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING

import redis.asyncio as aioredis
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import QuotaExceededError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class QuotaInfo(BaseModel):
    """Quota information."""

    user_type: str  # "anonymous" or "authenticated"
    remaining: int
    total: int
    reset_time: date | None = None


class QuotaService:
    """Service for managing user quotas."""

    # Redis key prefix
    ANONYMOUS_QUOTA_PREFIX = "anonymous_quota:"

    def __init__(
        self,
        redis_client: aioredis.Redis | None = None,
    ) -> None:
        """Initialize QuotaService.

        Args:
            redis_client: Redis client (default from URL)
        """
        self._redis = redis_client
        self._anonymous_free_quota = settings.anonymous_free_quota
        self._user_free_quota_weekly = settings.user_free_quota_weekly
        # In-memory storage for testing (used when redis is None)
        self._test_storage: dict[str, dict[str, str]] = {}

    def _get_week_start(self, dt: datetime | None = None) -> date:
        """Get start of week (Monday) for given datetime.

        Args:
            dt: Datetime to get week start for (default: now)

        Returns:
            Date of Monday of the week
        """
        if dt is None:
            dt = datetime.now(timezone.utc)

        # Get weekday (0=Monday, 6=Sunday)
        weekday = dt.weekday()
        # Subtract weekday days to get Monday
        week_start = dt - timedelta(days=weekday)
        return week_start.date()

    async def get_anonymous_quota(
        self,
        device_fingerprint: str,
        ip_address: str | None = None,
    ) -> QuotaInfo:
        """Get anonymous user quota information.

        Args:
            device_fingerprint: Device fingerprint
            ip_address: IP address (for new quota creation)

        Returns:
            QuotaInfo with quota details
        """
        key = f"{self.ANONYMOUS_QUOTA_PREFIX}{device_fingerprint}"

        # Check test storage first
        if not self._redis:
            if key in self._test_storage:
                data = self._test_storage[key]
                remaining = int(data.get("remaining", "0"))
                return QuotaInfo(
                    user_type="anonymous",
                    remaining=remaining,
                    total=self._anonymous_free_quota,
                    reset_time=None,
                )

            # Create new quota in test storage
            new_data = {
                "remaining": str(self._anonymous_free_quota),
                "ip": ip_address or "unknown",
            }
            self._test_storage[key] = new_data
            return QuotaInfo(
                user_type="anonymous",
                remaining=self._anonymous_free_quota,
                total=self._anonymous_free_quota,
                reset_time=None,
            )

        # Check Redis
        if self._redis:
            redis = self._redis
            data = await redis.hgetall(key)

            if data:
                remaining = int(data.get(b"remaining", b"0"))
                return QuotaInfo(
                    user_type="anonymous",
                    remaining=remaining,
                    total=self._anonymous_free_quota,
                    reset_time=None,
                )

            # Create new quota in Redis
            new_data = {
                "remaining": str(self._anonymous_free_quota),
                "ip": ip_address or "unknown",
            }
            await self._redis.hset(key, mapping=new_data)
            await self._redis.expire(key, settings.anonymous_quota_days * 86400)

            return QuotaInfo(
                user_type="anonymous",
                remaining=self._anonymous_free_quota,
                total=self._anonymous_free_quota,
                reset_time=None,
            )

        # Should not reach here
        raise QuotaExceededError(
            message="No storage available for quota",
            details={"device_fingerprint": device_fingerprint},
        )

    async def decrement_anonymous_quota(
        self,
        device_fingerprint: str,
    ) -> int:
        """Decrement anonymous user quota.

        Args:
            device_fingerprint: Device fingerprint

        Returns:
            Remaining quota after decrement

        Raises:
            QuotaExceededError: If quota is exhausted
        """
        key = f"{self.ANONYMOUS_QUOTA_PREFIX}{device_fingerprint}"

        if not self._redis:
            # Use test storage
            if key not in self._test_storage:
                self._test_storage[key] = {
                    "remaining": str(self._anonymous_free_quota),
                    "ip": "test",
                }

            current = int(self._test_storage[key].get("remaining", "0"))

            if current <= 0:
                raise QuotaExceededError(
                    message="Anonymous quota exceeded",
                    details={
                        "device_fingerprint": device_fingerprint,
                        "remaining": 0,
                    },
                )

            self._test_storage[key]["remaining"] = str(current - 1)
            return current - 1

        if self._redis:
            # Use Redis
            remaining = await self._redis.hincrby(key, "remaining", -1)
            # hincrby returns int in Python 3.11+
            if isinstance(remaining, bytes):
                remaining = int(remaining)

            if remaining < 0:
                # Revert decrement
                await self._redis.hincrby(key, "remaining", 1)
                raise QuotaExceededError(
                    message="Anonymous quota exceeded",
                    details={
                        "device_fingerprint": device_fingerprint,
                        "remaining": 0,
                    },
                )

            return remaining

        # Should not reach here
        raise QuotaExceededError(
            message="No storage available for quota",
            details={"device_fingerprint": device_fingerprint},
        )

    async def _get_redis(self) -> aioredis.Redis:
        """Get Redis client (lazy initialization).

        Returns:
            Redis client
        """
        if self._redis is None:
            self._redis = await aioredis.from_url(settings.redis_url)
        return self._redis

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None


def get_quota_service() -> QuotaService:
    """Get a QuotaService instance."""
    return QuotaService()
