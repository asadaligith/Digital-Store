"""
Checkout API schemas for request/response validation.

These schemas define the structure of data sent to and received from
the checkout API endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field
from src.models.address import AddressType
from src.models.checkout import ShippingMethodType, ShippingMethod, CheckoutTotals, OrderPreview


# ===== Request Schemas =====


class AddressRequest(BaseModel):
    """Schema for creating/updating an address."""

    type: AddressType = Field(default=AddressType.BOTH)
    full_name: str = Field(..., min_length=1, max_length=100)
    address_line1: str = Field(..., min_length=1, max_length=200)
    address_line2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(default="US", min_length=2, max_length=2)
    phone: str = Field(..., min_length=10, max_length=20)
    is_default: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "both",
                "full_name": "John Doe",
                "address_line1": "123 Main St",
                "address_line2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
                "phone": "+1-555-123-4567",
                "is_default": True,
            }
        }


class ValidateCartRequest(BaseModel):
    """Schema for validating cart before checkout."""

    cart_id: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {"cart_id": "507f1f77bcf86cd799439011"}
        }


class CalculateShippingRequest(BaseModel):
    """Schema for calculating shipping cost."""

    cart_id: str = Field(..., min_length=1)
    shipping_method: ShippingMethodType
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(default="US", min_length=2, max_length=2)

    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "507f1f77bcf86cd799439011",
                "shipping_method": "standard",
                "postal_code": "10001",
                "country": "US",
            }
        }


class CreateOrderPreviewRequest(BaseModel):
    """Schema for creating order preview."""

    cart_id: str = Field(..., min_length=1)
    shipping_address: AddressRequest
    shipping_method: ShippingMethodType

    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "507f1f77bcf86cd799439011",
                "shipping_address": {
                    "type": "both",
                    "full_name": "John Doe",
                    "address_line1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "US",
                    "phone": "+1-555-123-4567",
                },
                "shipping_method": "standard",
            }
        }


# ===== Response Schemas =====


class AddressResponse(BaseModel):
    """Schema for address response."""

    id: str = Field(..., alias="_id")
    user_id: Optional[str] = None
    type: AddressType
    full_name: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: str
    is_default: bool

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "user_id": None,
                "type": "both",
                "full_name": "John Doe",
                "address_line1": "123 Main St",
                "address_line2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
                "phone": "+1-555-123-4567",
                "is_default": True,
            }
        }


class CartValidationResponse(BaseModel):
    """Schema for cart validation response."""

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    items_count: int
    subtotal: float

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "errors": [],
                "warnings": ["Product 'Headphones' has limited stock (3 remaining)"],
                "items_count": 3,
                "subtotal": 129.99,
            }
        }


class ShippingMethodsResponse(BaseModel):
    """Schema for available shipping methods."""

    methods: list[ShippingMethod]

    class Config:
        json_schema_extra = {
            "example": {
                "methods": [
                    {
                        "method": "standard",
                        "name": "Standard Shipping",
                        "cost": 5.99,
                        "estimated_days": 5,
                        "description": "Delivery in 5-7 business days",
                    },
                    {
                        "method": "express",
                        "name": "Express Shipping",
                        "cost": 12.99,
                        "estimated_days": 2,
                        "description": "Delivery in 2-3 business days",
                    },
                ]
            }
        }


class OrderPreviewResponse(BaseModel):
    """Schema for order preview response."""

    preview: OrderPreview

    class Config:
        json_schema_extra = {
            "example": {
                "preview": {
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
        }
