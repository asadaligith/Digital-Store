"""
CORS (Cross-Origin Resource Sharing) middleware configuration.

Configures which origins are allowed to access the API.
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.

    Args:
        app: FastAPI application instance

    Configuration:
        - Allowed origins from settings.CORS_ORIGINS
        - Credentials enabled (for httpOnly cookies)
        - All methods allowed (GET, POST, PUT, DELETE, etc.)
        - All headers allowed
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,  # Required for httpOnly cookies
        allow_methods=["*"],      # Allow all HTTP methods
        allow_headers=["*"],      # Allow all headers
        expose_headers=["*"],     # Expose all headers to client
    )

    print(f"✅ CORS configured with origins: {settings.cors_origins_list}")
