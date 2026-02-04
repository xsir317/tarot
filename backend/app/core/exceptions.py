"""Custom exceptions for the application."""

from typing import Any


class AppError(Exception):
    """Base application exception."""

    def __init__(self, code: str, message: str, details: Any | None = None) -> None:
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class AuthenticationError(AppError):
    """Authentication related errors."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(code="AUTH_ERROR", message=message, details=details)


class AuthorizationError(AppError):
    """Authorization related errors."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(code="AUTHORIZATION_ERROR", message=message, details=details)


class QuotaExceededError(AppError):
    """Quota exceeded errors."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(code="QUOTA_ERROR", message=message, details=details)


class TarotError(AppError):
    """Tarot related errors."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(code="TAROT_ERROR", message=message, details=details)


class PaymentError(AppError):
    """Payment related errors."""

    def __init__(self, message: str, details: Any | None = None) -> None:
        super().__init__(code="PAYMENT_ERROR", message=message, details=details)
