"""Test quota management service."""

import pytest
from datetime import date, datetime, timezone

from app.services.quota_service import QuotaService
from app.core.exceptions import QuotaExceededError


@pytest.mark.asyncio
async def test_anonymous_user_gets_3_free_quota():
    """Test anonymous user gets 3 free quota."""
    service = QuotaService()
    device_fingerprint = "test-device-123"

    quota = await service.get_anonymous_quota(device_fingerprint)

    assert quota.user_type == "anonymous"
    assert quota.remaining == 3
    assert quota.total == 3


@pytest.mark.asyncio
async def test_decrement_anonymous_quota():
    """Test decrementing anonymous quota."""
    service = QuotaService()
    device_fingerprint = "test-device-456"

    remaining = await service.decrement_anonymous_quota(device_fingerprint)

    assert remaining == 2

    # Check quota again
    quota = await service.get_anonymous_quota(device_fingerprint)
    assert quota.remaining == 2


@pytest.mark.asyncio
async def test_decrement_anonymous_quota_exhausted():
    """Test decrementing when quota is exhausted."""
    service = QuotaService()
    device_fingerprint = "test-device-789"

    # Use all quota
    await service.decrement_anonymous_quota(device_fingerprint)
    await service.decrement_anonymous_quota(device_fingerprint)
    await service.decrement_anonymous_quota(device_fingerprint)

    # Try to decrement again - should raise error
    with pytest.raises(QuotaExceededError, match="Anonymous quota exceeded"):
        await service.decrement_anonymous_quota(device_fingerprint)


def test_get_week_start():
    """Test getting week start date."""
    service = QuotaService()

    # Monday
    monday = datetime(2026, 2, 3, 12, 0, 0, tzinfo=timezone.utc)
    week_start = service._get_week_start(monday)
    assert week_start == date(2026, 2, 2)

    # Wednesday - should return Monday
    wednesday = datetime(2026, 2, 5, 12, 0, 0, tzinfo=timezone.utc)
    week_start = service._get_week_start(wednesday)
    assert week_start == date(2026, 2, 2)

    # Sunday - should return previous Monday
    sunday = datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc)
    week_start = service._get_week_start(sunday)
    assert week_start == date(2026, 2, 2)
