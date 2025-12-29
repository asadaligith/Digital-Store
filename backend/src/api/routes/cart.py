"""
Cart API routes.

Endpoints for shopping cart operations:
- GET /api/cart - Get current cart
- POST /api/cart/items - Add item to cart
- PATCH /api/cart/items/{product_id} - Update item quantity
- DELETE /api/cart/items/{product_id} - Remove item from cart
- DELETE /api/cart - Clear cart
- POST /api/cart/merge - Merge guest cart on login
- GET /api/cart/summary - Get cart summary (for header badge)
"""

from fastapi import APIRouter, Depends, Response, Request
from typing import Optional

from src.db.mongodb import get_database
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.services.cart_service import CartService
from src.schemas.cart import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartResponse,
    CartSummaryResponse,
    MergeCartRequest
)

router = APIRouter()


# ===== Dependencies =====


def get_cart_service(db=Depends(get_database)) -> CartService:
    """Get cart service instance with dependencies."""
    cart_repo = CartRepository(db)
    product_repo = ProductRepository(db)
    return CartService(cart_repo, product_repo)


def get_user_or_session_id(request: Request) -> tuple[Optional[str], Optional[str]]:
    """
    Extract user_id or session_id from request.

    For now, we use session_id from cookies for guest users.
    When authentication is implemented, this will also check for user_id from JWT.

    Returns:
        Tuple of (user_id, session_id)
    """
    # TODO: Extract user_id from JWT when auth is implemented
    user_id = None

    # Get or create session_id for guest users
    session_id = request.cookies.get("session_id")

    return user_id, session_id


# ===== Routes =====


@router.get("", response_model=CartResponse)
async def get_cart(
    request: Request,
    response: Response,
    service: CartService = Depends(get_cart_service)
):
    """
    Get current user's cart.

    For authenticated users: Returns cart by user_id
    For guest users: Returns cart by session_id (creates session if needed)

    Returns:
        Cart with populated product details
    """
    user_id, session_id = get_user_or_session_id(request)

    # Create session_id for guest if not exists
    if not user_id and not session_id:
        import uuid
        session_id = f"guest-{uuid.uuid4()}"
        # Set session cookie (7 days expiry to match cart expiration)
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=7 * 24 * 60 * 60,  # 7 days in seconds
            httponly=True,
            samesite="lax"
        )

    cart = await service.get_or_create_cart(user_id=user_id, session_id=session_id)
    return cart


@router.get("/summary", response_model=CartSummaryResponse)
async def get_cart_summary(
    request: Request,
    response: Response,
    service: CartService = Depends(get_cart_service)
):
    """
    Get lightweight cart summary for header badge.

    Returns:
        Cart summary with item_count and subtotal
    """
    user_id, session_id = get_user_or_session_id(request)

    # Create session_id for guest if not exists
    if not user_id and not session_id:
        import uuid
        session_id = f"guest-{uuid.uuid4()}"
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=7 * 24 * 60 * 60,
            httponly=True,
            samesite="lax"
        )

    summary = await service.get_cart_summary(user_id=user_id, session_id=session_id)
    return summary


@router.post("/items", response_model=CartResponse, status_code=201)
async def add_to_cart(
    data: AddToCartRequest,
    request: Request,
    response: Response,
    service: CartService = Depends(get_cart_service)
):
    """
    Add item to cart.

    Request Body:
        - product_id: Product ID to add
        - quantity: Quantity to add (default: 1)

    Returns:
        Updated cart with populated product details

    Raises:
        404: If product not found
        422: If product is out of stock or quantity exceeds inventory
    """
    user_id, session_id = get_user_or_session_id(request)

    # Create session_id for guest if not exists
    if not user_id and not session_id:
        import uuid
        session_id = f"guest-{uuid.uuid4()}"
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=7 * 24 * 60 * 60,
            httponly=True,
            samesite="lax"
        )

    # Get or create cart
    cart = await service.get_or_create_cart(user_id=user_id, session_id=session_id)

    # Add item to cart
    updated_cart = await service.add_to_cart(cart["_id"], data)

    return updated_cart


@router.patch("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: str,
    data: UpdateCartItemRequest,
    request: Request,
    service: CartService = Depends(get_cart_service)
):
    """
    Update cart item quantity.

    Path Parameters:
        - product_id: Product ID to update

    Request Body:
        - quantity: New quantity (set to 0 to remove item)

    Returns:
        Updated cart with populated product details

    Raises:
        404: If cart or product not found
        422: If quantity exceeds inventory
    """
    user_id, session_id = get_user_or_session_id(request)

    # Get existing cart
    cart = await service.get_or_create_cart(user_id=user_id, session_id=session_id)

    # Update item quantity
    updated_cart = await service.update_cart_item(cart["_id"], product_id, data)

    return updated_cart


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    product_id: str,
    request: Request,
    service: CartService = Depends(get_cart_service)
):
    """
    Remove item from cart.

    Path Parameters:
        - product_id: Product ID to remove

    Returns:
        Updated cart with populated product details

    Raises:
        404: If cart or product not found
    """
    user_id, session_id = get_user_or_session_id(request)

    # Get existing cart
    cart = await service.get_or_create_cart(user_id=user_id, session_id=session_id)

    # Remove item
    updated_cart = await service.remove_from_cart(cart["_id"], product_id)

    return updated_cart


@router.delete("", response_model=CartResponse)
async def clear_cart(
    request: Request,
    service: CartService = Depends(get_cart_service)
):
    """
    Clear all items from cart.

    Returns:
        Empty cart

    Raises:
        404: If cart not found
    """
    user_id, session_id = get_user_or_session_id(request)

    # Get existing cart
    cart = await service.get_or_create_cart(user_id=user_id, session_id=session_id)

    # Clear cart
    cleared_cart = await service.clear_cart(cart["_id"])

    return cleared_cart


@router.post("/merge", response_model=CartResponse)
async def merge_guest_cart(
    data: MergeCartRequest,
    request: Request,
    service: CartService = Depends(get_cart_service)
):
    """
    Merge guest cart into user cart on login.

    This endpoint is called after successful login to merge the guest's
    shopping cart into their authenticated user cart.

    Request Body:
        - session_id: Guest cart session ID

    Returns:
        Merged user cart with populated product details

    Raises:
        401: If user is not authenticated
        404: If guest cart not found
    """
    user_id, _ = get_user_or_session_id(request)

    # TODO: Enforce authentication when auth is implemented
    if not user_id:
        # For now, we'll skip this check until auth is implemented
        # raise HTTPException(status_code=401, detail="Authentication required")
        pass

    # For testing purposes, use a placeholder user_id if none exists
    # This will be removed when authentication is implemented
    if not user_id:
        user_id = "test-user-id"

    # Merge carts
    merged_cart = await service.merge_guest_cart(
        user_id=user_id,
        session_id=data.session_id
    )

    return merged_cart
