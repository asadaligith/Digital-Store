"""
Checkout models for order processing.

Contains models for shipping methods, order previews,
and checkout-related data structures.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ShippingMethodType(str, Enum):
    """Shipping method enumeration."""
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"


class ShippingMethod(BaseModel):
    """
    Shipping method with cost and delivery estimate.

    Attributes:
        method: Shipping method type
        name: Display name
        cost: Shipping cost
        estimated_days: Estimated delivery days
        description: Method description
    """

    method: ShippingMethodType
    name: str = Field(..., min_length=1)
    cost: float = Field(..., ge=0)
    estimated_days: int = Field(..., ge=1)
    description: str = Field(default="")

    class Config:
        json_schema_extra = {
            "example": {
                "method": "standard",
                "name": "Standard Shipping",
                "cost": 5.99,
                "estimated_days": 5,
                "description": "Delivery in 5-7 business days",
            }
        }


class CheckoutTotals(BaseModel):
    """
    Checkout totals breakdown.

    Attributes:
        subtotal: Cart items subtotal
        shipping: Shipping cost
        tax: Sales tax
        discount: Discount amount (if any)
        total: Final total
    """

    subtotal: float = Field(..., ge=0)
    shipping: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)
    discount: float = Field(default=0, ge=0)
    total: float = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "subtotal": 129.99,
                "shipping": 5.99,
                "tax": 10.88,
                "discount": 0,
                "total": 146.86,
            }
        }


class OrderPreview(BaseModel):
    """
    Order preview for checkout review.

    Contains all information needed for order confirmation
    before payment processing.

    Attributes:
        cart_id: Reference to shopping cart
        items_count: Number of items
        totals: Breakdown of totals
        shipping_address: Shipping address data
        shipping_method: Selected shipping method
        can_proceed: Whether order can proceed to payment
        validation_errors: Any validation errors
    """

    cart_id: str
    items_count: int = Field(..., ge=0)
    totals: CheckoutTotals
    shipping_address: Optional[dict] = None
    shipping_method: Optional[ShippingMethod] = None
    can_proceed: bool = Field(default=False)
    validation_errors: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "507f1f77bcf86cd799439011",
                "items_count": 3,
                "totals": {
                    "subtotal": 129.99,
                    "shipping": 5.99,
                    "tax": 10.88,
                    "discount": 0,
                    "total": 146.86,
                },
                "shipping_address": {
                    "full_name": "John Doe",
                    "address_line1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "US",
                },
                "shipping_method": {
                    "method": "standard",
                    "name": "Standard Shipping",
                    "cost": 5.99,
                    "estimated_days": 5,
                },
                "can_proceed": True,
                "validation_errors": [],
            }
        }


# Predefined shipping methods
SHIPPING_METHODS = [
    ShippingMethod(
        method=ShippingMethodType.STANDARD,
        name="Standard Shipping",
        cost=5.99,
        estimated_days=5,
        description="Delivery in 5-7 business days",
    ),
    ShippingMethod(
        method=ShippingMethodType.EXPRESS,
        name="Express Shipping",
        cost=12.99,
        estimated_days=2,
        description="Delivery in 2-3 business days",
    ),
    ShippingMethod(
        method=ShippingMethodType.OVERNIGHT,
        name="Overnight Shipping",
        cost=24.99,
        estimated_days=1,
        description="Next business day delivery",
    ),
]
