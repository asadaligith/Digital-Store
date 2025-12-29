"""
Payment API schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field
from src.models.payment import PaymentStatus


# ===== Request Schemas =====


class ProcessPaymentRequest(BaseModel):
    """Schema for processing a payment."""

    order_id: str = Field(..., min_length=1)
    payment_method_id: str = Field(..., min_length=1, description="Stripe PaymentMethod ID")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "507f1f77bcf86cd799439011",
                "payment_method_id": "pm_1234567890abcdef",
            }
        }


# ===== Response Schemas =====


class PaymentIntentResponse(BaseModel):
    """Schema for payment intent response."""

    client_secret: str
    amount: float
    currency: str

    class Config:
        json_schema_extra = {
            "example": {
                "client_secret": "pi_1234567890abcdef_secret_1234567890abcdef",
                "amount": 286.77,
                "currency": "usd",
            }
        }


class PaymentResponse(BaseModel):
    """Schema for payment response."""

    id: str = Field(..., alias="_id")
    order_id: str
    transaction_id: str
    status: PaymentStatus
    amount: float
    currency: str
    card_last4: Optional[str] = None
    card_brand: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "order_id": "507f1f77bcf86cd799439012",
                "transaction_id": "pi_1234567890abcdef",
                "status": "completed",
                "amount": 286.77,
                "currency": "USD",
                "card_last4": "4242",
                "card_brand": "Visa",
            }
        }
