"""Test User model."""

import pytest
from datetime import datetime

from app.models.user import User, UserQuota
from app.models.base import Base


def test_user_model_attributes():
    """Test User model has correct attributes."""
    assert hasattr(User, "id")
    assert hasattr(User, "email")
    assert hasattr(User, "phone")
    assert hasattr(User, "password_hash")
    assert hasattr(User, "nickname")
    assert hasattr(User, "gender")
    assert hasattr(User, "is_active")
    assert hasattr(User, "created_at")
    assert hasattr(User, "updated_at")


def test_user_model_table_name():
    """Test User model has correct table name."""
    assert User.__tablename__ == "users"


def test_user_quota_model_attributes():
    """Test UserQuota model has correct attributes."""
    assert hasattr(UserQuota, "id")
    assert hasattr(UserQuota, "user_id")
    assert hasattr(UserQuota, "remaining")
    assert hasattr(UserQuota, "total")
    assert hasattr(UserQuota, "week_start")


def test_user_quota_model_table_name():
    """Test UserQuota model has correct table name."""
    assert UserQuota.__tablename__ == "user_quotas"


def test_base_model_has_timestamps():
    """Test Base model has timestamp attributes."""
    assert hasattr(Base, "created_at")
    assert hasattr(Base, "updated_at")
