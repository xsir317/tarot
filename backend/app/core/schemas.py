"""Common response schemas."""

from pydantic import BaseModel, Field
from typing import Any, Generic, TypeVar


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response."""

    success: bool = Field(default=True, description="Always true for success responses")
    data: T = Field(description="Response data")
    message: str | None = Field(default=None, description="Optional message")


class ErrorDetail(BaseModel):
    """Error detail."""

    code: str = Field(description="Error code")
    message: str = Field(description="Error message")
    details: dict[str, Any] | None = Field(default=None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = Field(default=False, description="Always false for error responses")
    error: ErrorDetail = Field(description="Error details")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Application status")
    version: str = Field(description="Application version")
