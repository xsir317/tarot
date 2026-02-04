"""Payment-related models."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.reading import Reading


class Subscription(Base):
    """Subscription model."""

    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    stripe_subscription_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    plan: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="monthly/yearly",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="active/canceled/past_due/expired",
    )

    daily_limit: Mapped[int] = mapped_column(default=200, nullable=False)

    weekly_limit: Mapped[int] = mapped_column(default=700, nullable=False)

    current_period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    current_period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")


class OneTimePayment(Base):
    """One-time payment model."""

    __tablename__ = "one_time_payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    user_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    stripe_payment_intent_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="Amount in cents")

    currency: Mapped[str] = mapped_column(String(3), default="usd")

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="pending/succeeded/canceled/failed",
    )

    reading_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("readings.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    reading: Mapped["Reading"] = relationship("Reading", back_populates="payment")
