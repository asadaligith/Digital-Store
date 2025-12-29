"""
Order model for MongoDB.

Represents a customer order with:
- Order identification and tracking
- Customer information (user or guest)
- Order items with pricing
- Shipping details
- Payment information
- Order status and timestamps
"""

from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from src.models.address import Address


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """
    Individual item in an order (embedded).

    Attributes:
        product_id: Reference to product
        product_name: Product name (denormalized for history)
        product_sku: Product SKU (denormalized)
        quantity: Quantity ordered
        price_at_purchase: Price at time of purchase
        subtotal: Item subtotal (quantity × price)
    """

    product_id: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    product_sku: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    price_at_purchase: float = Field(..., gt=0)
    subtotal: float = Field(..., gt=0)

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


class Order(BaseModel):
    """
    Order model representing a customer purchase.

    Attributes:
        id: Unique order identifier
        order_number: Human-readable order number
        user_id: Reference to user (optional for guest)
        guest_email: Guest email (for order confirmation)
        status: Order status
        items: List of order items
        shipping_address: Embedded shipping address
        shipping_method: Shipping method type
        shipping_cost: Shipping cost
        subtotal: Order subtotal
        tax_amount: Tax amount
        total_amount: Total order amount
        payment_id: Reference to payment
        estimated_delivery_date: Estimated delivery
        tracking_number: Shipping tracking number
        notes: Order notes
        created_at: Order creation timestamp
        updated_at: Last update timestamp
        shipped_at: Shipping timestamp
        delivered_at: Delivery timestamp
        cancelled_at: Cancellation timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    order_number: str = Field(..., min_length=1)
    user_id: Optional[str] = None
    guest_email: Optional[str] = None
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    items: List[OrderItem] = Field(..., min_items=1)
    shipping_address: dict = Field(...)  # Embedded address
    shipping_method: str = Field(..., min_length=1)
    shipping_cost: float = Field(..., ge=0)
    subtotal: float = Field(..., gt=0)
    tax_amount: float = Field(..., ge=0)
    total_amount: float = Field(..., gt=0)
    payment_id: Optional[str] = None
    estimated_delivery_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "order_number": "ORD-20240115-001234",
                "user_id": "507f1f77bcf86cd799439011",
                "guest_email": None,
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
                    "country": "US",
                    "phone": "+1-555-123-4567",
                },
                "shipping_method": "standard",
                "shipping_cost": 5.99,
                "subtotal": 259.98,
                "tax_amount": 20.80,
                "total_amount": 286.77,
                "payment_id": None,
                "estimated_delivery_date": "2024-01-22T00:00:00Z",
            }
        }

    @field_validator("guest_email", mode="before")
    @classmethod
    def validate_guest_email(cls, v, values):
        """Ensure either user_id or guest_email is provided."""
        # This will be validated in the service layer
        return v

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        data.pop("_id", None)
        return data
