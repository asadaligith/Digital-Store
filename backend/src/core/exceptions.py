"""
Custom exception classes for structured error handling.

These exceptions are used throughout the application to provide
consistent error responses via the error handling middleware.
"""

from typing import Optional, Dict, Any


class AppException(Exception):
    """Base exception for all application exceptions"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """
    Raised when a requested resource is not found.

    HTTP Status: 404 Not Found
    """

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)


class ValidationException(AppException):
    """
    Raised when input validation fails.

    HTTP Status: 400 Bad Request
    """

    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class UnauthorizedException(AppException):
    """
    Raised when authentication is required but not provided or invalid.

    HTTP Status: 401 Unauthorized
    """

    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class ForbiddenException(AppException):
    """
    Raised when user doesn't have permission to access a resource.

    HTTP Status: 403 Forbidden
    """

    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)


class DuplicateException(AppException):
    """
    Raised when attempting to create a resource that already exists.

    HTTP Status: 409 Conflict
    """

    def __init__(self, message: str = "Resource already exists", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class PaymentException(AppException):
    """
    Raised when payment processing fails.

    HTTP Status: 402 Payment Required
    """

    def __init__(self, message: str = "Payment processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=402, details=details)


class RateLimitException(AppException):
    """
    Raised when rate limit is exceeded.

    HTTP Status: 429 Too Many Requests
    """

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=429, details=details)


class InternalServerException(AppException):
    """
    Raised for unexpected internal server errors.

    HTTP Status: 500 Internal Server Error
    """

    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)
