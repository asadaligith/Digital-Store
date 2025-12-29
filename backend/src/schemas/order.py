"""
Order API schemas for request/response validation.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from src.models.order import OrderStatus, OrderItem


# ===== Request Schemas =====


class CreateOrderRequest(BaseModel):
    """Schema for creating an order."""

    cart_id: str = Field(..., min_length=1)
    guest_email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {
                "cart_id": "507f1f77bcf86cd799439011",
                "guest_email": "guest@example.com",
            }
        }


# ===== Response Schemas =====


class OrderItemResponse(BaseModel):
    """Schema for order item in response."""

    product_id: str
    product_name: str
    product_sku: str
    quantity: int
    price_at_purchase: float
    subtotal: float

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "507f1f77bcf86cd799439012",
                "product_name": "Wireless Bluetooth Headphones",
                "product_sku": "WBH-001",
                "quantity": 2,
                "price_at_purchase": 129.99,
                "subtotal": 259.98,
            }
        }


class OrderResponse(BaseModel):
    """Schema for order response."""

    id: str = Field(..., alias="_id")
    order_number: str
    user_id: Optional[str] = None
    guest_email: Optional[str] = None
    status: OrderStatus
    items: List[OrderItemResponse]
    shipping_address: dict
    shipping_method: str
    shipping_cost: float
    subtotal: float
    tax_amount: float
    total_amount: float
    payment_id: Optional[str] = None
    estimated_delivery_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "order_number": "ORD-20240115-001234",
                "user_id": None,
                "guest_email": "guest@example.com",
                "status": "pending",
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439012",
                        "product_name": "Wireless Bluetooth Headphones",
                        "product_sku": "WBH-001",
                        "quantity": 2,
                        "price_at_purchase": 129.99,
                        "subtotal": 259.98,
                    }
                ],
                "shipping_address": {
                    "full_name": "John Doe",
                    "address_line1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                },
                "shipping_method": "standard",
                "shipping_cost": 5.99,
                "subtotal": 259.98,
                "tax_amount": 20.80,
                "total_amount": 286.77,
                "payment_id": None,
                "estimated_delivery_date": "2024-01-22T00:00:00Z",
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
            }
        }


class OrderListResponse(BaseModel):
    """Schema for list of orders."""

    orders: List[OrderResponse]
    total: int
    page: int
    pages: int

    class Config:
        json_schema_extra = {
            "example": {
                "orders": [],
                "total": 0,
                "page": 1,
                "pages": 1,
            }
        }
