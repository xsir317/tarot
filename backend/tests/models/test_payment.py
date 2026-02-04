"""Test Payment models."""

from app.models.payment import Subscription, OneTimePayment


def test_subscription_model_attributes():
    """Test Subscription model has correct attributes."""
    assert hasattr(Subscription, "id")
    assert hasattr(Subscription, "user_id")
    assert hasattr(Subscription, "stripe_subscription_id")
    assert hasattr(Subscription, "plan")
    assert hasattr(Subscription, "status")
    assert hasattr(Subscription, "daily_limit")
    assert hasattr(Subscription, "weekly_limit")
    assert hasattr(Subscription, "current_period_start")
    assert hasattr(Subscription, "current_period_end")
    assert hasattr(Subscription, "cancel_at_period_end")


def test_subscription_model_table_name():
    """Test Subscription model has correct table name."""
    assert Subscription.__tablename__ == "subscriptions"


def test_one_time_payment_model_attributes():
    """Test OneTimePayment model has correct attributes."""
    assert hasattr(OneTimePayment, "id")
    assert hasattr(OneTimePayment, "user_id")
    assert hasattr(OneTimePayment, "stripe_payment_intent_id")
    assert hasattr(OneTimePayment, "amount")
    assert hasattr(OneTimePayment, "currency")
    assert hasattr(OneTimePayment, "status")
    assert hasattr(OneTimePayment, "reading_id")


def test_one_time_payment_model_table_name():
    """Test OneTimePayment model has correct table name."""
    assert OneTimePayment.__tablename__ == "one_time_payments"
