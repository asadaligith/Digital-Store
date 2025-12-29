"""
Security utilities for JWT token management and password hashing.

This module provides cryptographic functions for:
- JWT access and refresh token generation/verification
- Password hashing with bcrypt (≥12 rounds)
- Secure token creation
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from src.core.config import settings

# Password hashing context with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS  # ≥12 rounds as per constitution
)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with configured rounds.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Security:
        - Uses bcrypt algorithm
        - Configured with ≥12 rounds (see settings.BCRYPT_ROUNDS)
        - Salt is automatically generated and included in hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_access_token(data: Dict[str, Any]) -> str:
    """
    Generate JWT access token with short expiration (15 minutes).

    Args:
        data: Payload data to encode in token (typically user_id, email)

    Returns:
        Encoded JWT token string

    Token Claims:
        - exp: Expiration time (15 minutes from now)
        - iat: Issued at time
        - sub: Subject (typically user_id)
        - ... (custom data from input)
    """
    to_encode = data.copy()

    # Set expiration time
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def generate_refresh_token(data: Dict[str, Any]) -> str:
    """
    Generate JWT refresh token with long expiration (7 days).

    Args:
        data: Payload data to encode in token (typically user_id)

    Returns:
        Encoded JWT refresh token string

    Token Claims:
        - exp: Expiration time (7 days from now)
        - iat: Issued at time
        - type: "refresh" (to distinguish from access tokens)
        - ... (custom data from input)
    """
    to_encode = data.copy()

    # Set expiration time
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    # Encode token using refresh secret
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(
    token: str,
    is_refresh_token: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token string to verify
        is_refresh_token: If True, uses refresh token secret key

    Returns:
        Decoded token payload if valid, None if invalid/expired

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        secret_key = (
            settings.JWT_REFRESH_SECRET_KEY
            if is_refresh_token
            else settings.JWT_SECRET_KEY
        )

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None


def get_password_strength(password: str) -> Dict[str, Any]:
    """
    Evaluate password strength.

    Args:
        password: Password to evaluate

    Returns:
        Dictionary with strength metrics:
            - strength: "weak", "medium", "strong"
            - length: Password length
            - has_upper: Has uppercase letters
            - has_lower: Has lowercase letters
            - has_digit: Has digits
            - has_special: Has special characters
    """
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    strength_score = sum([
        len(password) >= 8,
        len(password) >= 12,
        has_upper,
        has_lower,
        has_digit,
        has_special
    ])

    if strength_score >= 5:
        strength = "strong"
    elif strength_score >= 3:
        strength = "medium"
    else:
        strength = "weak"

    return {
        "strength": strength,
        "length": len(password),
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special
    }
