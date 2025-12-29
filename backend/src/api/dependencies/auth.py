"""
Authentication dependencies for protected routes.

Provides FastAPI dependencies to extract and validate JWT tokens from requests.
"""

from fastapi import Depends, Request, Header
from typing import Optional, Dict, Any
from src.core.exceptions import UnauthorizedException
from src.core.security import verify_token


async def get_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract JWT token from Authorization header.

    Args:
        authorization: Authorization header value (format: "Bearer <token>")

    Returns:
        JWT token string or None if not present

    Raises:
        UnauthorizedException: If authorization header format is invalid
    """
    if not authorization:
        return None

    # Check format: "Bearer <token>"
    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise UnauthorizedException(
            message="Invalid authorization header format. Expected: 'Bearer <token>'"
        )

    return parts[1]


async def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extract JWT token from httpOnly cookie.

    Args:
        request: FastAPI request object

    Returns:
        JWT token string or None if cookie not present
    """
    return request.cookies.get("access_token")


async def get_current_user_optional(
    token_header: Optional[str] = Depends(get_token_from_header),
    request: Request = None
) -> Optional[Dict[str, Any]]:
    """
    Get current user from JWT token (optional - doesn't require authentication).

    Checks both Authorization header and httpOnly cookies.

    Args:
        token_header: Token from Authorization header
        request: FastAPI request (for cookie access)

    Returns:
        User payload from token or None if not authenticated
    """
    # Try Authorization header first, then cookie
    token = token_header or (await get_token_from_cookie(request) if request else None)

    if not token:
        return None

    # Verify and decode token
    payload = verify_token(token, is_refresh_token=False)

    if not payload:
        return None

    return payload


async def get_current_user(
    user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
) -> Dict[str, Any]:
    """
    Get current user from JWT token (REQUIRED - raises exception if not authenticated).

    Use this dependency for protected routes that require authentication.

    Args:
        user: User payload from get_current_user_optional

    Returns:
        User payload from token

    Raises:
        UnauthorizedException: If user is not authenticated
    """
    if not user:
        raise UnauthorizedException(
            message="Authentication required. Please provide a valid access token."
        )

    return user


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current active user (not disabled/locked).

    Args:
        current_user: User payload from get_current_user

    Returns:
        User payload if user is active

    Raises:
        UnauthorizedException: If user account is disabled
    """
    # Check if user is active (this will be enhanced when user repository is implemented)
    if current_user.get("is_active") is False:
        raise UnauthorizedException(
            message="User account is disabled"
        )

    return current_user


def require_roles(*required_roles: str):
    """
    Dependency factory to check user has required roles.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_roles("admin"))])
        async def admin_endpoint():
            ...

    Args:
        *required_roles: Role names required to access endpoint

    Returns:
        Dependency function that validates user roles
    """
    async def check_roles(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_roles = current_user.get("roles", [])

        if not any(role in user_roles for role in required_roles):
            raise UnauthorizedException(
                message=f"Insufficient permissions. Required roles: {', '.join(required_roles)}"
            )

        return current_user

    return check_roles
