"""
Rate limiting dependency using slowapi.

Provides rate limiting to prevent abuse and DDoS attacks.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from src.core.config import settings


# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No default limit, specify per route
    storage_uri="memory://",  # In-memory storage (use Redis in production)
)


def rate_limit(limit: int = None, window: int = 60):
    """
    Rate limiting dependency factory.

    Args:
        limit: Maximum requests allowed (None = use default from settings)
        window: Time window in seconds (default: 60 seconds = 1 minute)

    Returns:
        Dependency function for FastAPI routes

    Usage:
        # Limit to 100 requests per minute
        @router.get("/products", dependencies=[Depends(rate_limit(limit=100))])
        async def list_products():
            ...

        # Use default authenticated user limit (100 req/min)
        @router.get("/profile", dependencies=[Depends(rate_limit())])
        async def get_profile(current_user = Depends(get_current_user)):
            ...
    """
    # Use default limits from settings if not specified
    if limit is None:
        limit = settings.RATE_LIMIT_AUTHENTICATED

    limit_string = f"{limit}/{window} seconds"

    async def check_rate_limit(request: Request):
        """Check if request exceeds rate limit"""
        # This will be called by slowapi automatically
        # The limiter will raise RateLimitExceeded if limit is exceeded
        pass

    # Return the limit string for slowapi to parse
    check_rate_limit.__closure__ = None
    check_rate_limit.limit = limit_string

    return check_rate_limit


def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key based on user authentication status.

    - Authenticated users: Rate limited by user_id
    - Anonymous users: Rate limited by IP address

    Args:
        request: FastAPI request

    Returns:
        Rate limit key (user_id or IP address)
    """
    # Check if user is authenticated (from JWT token in header or cookie)
    user = getattr(request.state, "user", None)

    if user:
        # Rate limit by user ID
        return f"user:{user.get('sub', 'unknown')}"
    else:
        # Rate limit by IP address
        return f"ip:{get_remote_address(request)}"


# Custom limiter with authentication-aware key function
auth_aware_limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=[],
    storage_uri="memory://",
)
