"""Reading-related models."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.payment import OneTimePayment


class Reading(Base):
    """Tarot reading model."""

    __tablename__ = "readings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    user_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)

    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)

    language: Mapped[str] = mapped_column(String(10), default="zh", nullable=False)

    cards: Mapped[dict] = mapped_column(JSON, nullable=False)

    individual_interpretations: Mapped[dict] = mapped_column(JSON, nullable=False)

    overall_interpretation: Mapped[str] = mapped_column(Text, nullable=False)

    quota_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="free/subscription/one_time",
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="readings")
    payment: Mapped["OneTimePayment"] = relationship("OneTimePayment", back_populates="reading")
