"""User-related models."""

from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Date, Index, String, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.payment import Subscription
    from app.models.reading import Reading


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="male/female/other/prefer_not_to_say",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default="true",
        default=True,
        nullable=False,
    )

    # Relationships
    quota: Mapped["UserQuota"] = relationship(
        "UserQuota",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    readings: Mapped[list["Reading"]] = relationship(
        "Reading",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_users_email", "email", postgresql_where="email IS NOT NULL"),
        Index("ix_users_phone", "phone", postgresql_where="phone IS NOT NULL"),
    )


class UserQuota(Base):
    """User free quota model."""

    __tablename__ = "user_quotas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    remaining: Mapped[int] = mapped_column(
        server_default="3",
        default=3,
        nullable=False,
    )

    total: Mapped[int] = mapped_column(
        server_default="3",
        default=3,
        nullable=False,
    )

    week_start: Mapped[date] = mapped_column(
        Date,
        default=lambda: datetime.now(timezone.utc).date(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="quota")


class AnonymousQuota(Base):
    """Anonymous user quota model."""

    __tablename__ = "anonymous_quotas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    device_fingerprint: Mapped[str] = mapped_column(String(255), nullable=False)

    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)

    remaining: Mapped[int] = mapped_column(
        server_default="3",
        default=3,
        nullable=False,
    )

    __table_args__ = (
        Index("ix_anonymous_quotas_fingerprint", "device_fingerprint"),
    )
