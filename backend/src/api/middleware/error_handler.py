"""
Global error handling middleware for consistent error responses.

Catches all exceptions and returns structured JSON error responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import AppException


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler middleware.

    Catches all exceptions and returns consistent JSON error responses:
    {
        "error": {
            "code": "ERROR_CODE",
            "message": "Human readable message",
            "details": {...},  // Optional additional details
            "path": "/api/endpoint"
        }
    }

    Args:
        request: FastAPI request
        call_next: Next middleware/route handler

    Returns:
        JSONResponse with error details or successful response
    """
    try:
        return await call_next(request)

    except AppException as e:
        # Custom application exceptions
        return JSONResponse(
            status_code=e.status_code,
            content={
                "error": {
                    "code": e.__class__.__name__.replace("Exception", "").upper(),
                    "message": e.message,
                    "details": e.details,
                    "path": request.url.path
                }
            }
        )

    except ValueError as e:
        # Value errors (validation)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": "INVALID_VALUE",
                    "message": str(e),
                    "path": request.url.path
                }
            }
        )

    except Exception as e:
        # Unexpected errors - log and return generic error
        # In production, log to external service (Sentry, CloudWatch, etc.)
        print(f"❌ Unexpected error: {str(e)}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "path": request.url.path
                }
            }
        )
