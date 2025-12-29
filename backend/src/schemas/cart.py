"""
Cart API schemas for request/response validation.

These schemas define the structure of data sent to and received from
the cart API endpoints.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ===== Request Schemas =====


class AddToCartRequest(BaseModel):
    """Schema for adding item to cart."""

    product_id: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "507f1f77bcf86cd799439012",
                "quantity": 2,
            }
        }


class UpdateCartItemRequest(BaseModel):
    """Schema for updating cart item quantity."""

    quantity: int = Field(..., ge=0, le=100, description="Set to 0 to remove item")

    class Config:
        json_schema_extra = {"example": {"quantity": 3}}


class MergeCartRequest(BaseModel):
    """Schema for merging guest cart with user cart on login."""

    session_id: str = Field(..., min_length=1, description="Guest cart session ID")

    class Config:
        json_schema_extra = {"example": {"session_id": "guest-abc-123-xyz"}}


# ===== Response Schemas =====


class CartItemResponse(BaseModel):
    """Schema for cart item in response."""

    product_id: str
    quantity: int
    price: float

    # Product details (populated from product lookup)
    product_name: Optional[str] = None
    product_slug: Optional[str] = None
    product_image: Optional[str] = None
    product_in_stock: Optional[bool] = None
    product_inventory: Optional[int] = None

    # Computed fields
    item_total: float = Field(description="Quantity * Price")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "507f1f77bcf86cd799439012",
                "quantity": 2,
                "price": 129.99,
                "product_name": "Wireless Bluetooth Headphones",
                "product_slug": "wireless-bluetooth-headphones",
                "product_image": "https://images.unsplash.com/...",
                "product_in_stock": True,
                "product_inventory": 50,
                "item_total": 259.98,
            }
        }


class CartResponse(BaseModel):
    """Schema for cart response with populated product details."""

    id: str = Field(..., alias="_id")
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    items: List[CartItemResponse]
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    # Computed fields
    item_count: int = Field(description="Total number of items")
    subtotal: float = Field(description="Cart subtotal")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "user_id": None,
                "session_id": "guest-abc-123-xyz",
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439012",
                        "quantity": 2,
                        "price": 129.99,
                        "product_name": "Wireless Bluetooth Headphones",
                        "product_slug": "wireless-bluetooth-headphones",
                        "product_image": "https://...",
                        "product_in_stock": True,
                        "product_inventory": 50,
                        "item_total": 259.98,
                    }
                ],
                "expires_at": "2024-01-22T10:00:00Z",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "item_count": 2,
                "subtotal": 259.98,
            }
        }


class CartSummaryResponse(BaseModel):
    """Lightweight cart summary (for header badge, etc.)."""

    item_count: int = Field(description="Total number of items")
    subtotal: float = Field(description="Cart subtotal")

    class Config:
        json_schema_extra = {"example": {"item_count": 3, "subtotal": 389.97}}
