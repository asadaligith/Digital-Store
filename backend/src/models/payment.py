"""
Payment model for MongoDB.

Represents a payment transaction with:
- Payment method and provider
- Transaction details
- Payment status
- Card information (last 4 digits)
- Refund information
"""

from datetime import datetime
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"


class PaymentProvider(str, Enum):
    """Payment provider enumeration."""
    STRIPE = "stripe"
    PAYPAL = "paypal"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(BaseModel):
    """
    Payment model representing a payment transaction.

    Attributes:
        id: Unique payment identifier
        order_id: Reference to order
        payment_method: Payment method used
        payment_provider: Payment provider
        transaction_id: Provider transaction ID
        status: Payment status
        amount: Payment amount
        currency: Currency code
        card_last4: Last 4 digits of card
        card_brand: Card brand (Visa, Mastercard, etc.)
        failure_reason: Reason for payment failure
        refund_amount: Amount refunded
        refund_reason: Reason for refund
        metadata: Additional metadata
        created_at: Payment creation timestamp
        completed_at: Payment completion timestamp
        failed_at: Payment failure timestamp
        refunded_at: Refund timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    order_id: str = Field(..., min_length=1)
    payment_method: PaymentMethod
    payment_provider: PaymentProvider
    transaction_id: str = Field(..., min_length=1)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    card_last4: Optional[str] = Field(None, min_length=4, max_length=4)
    card_brand: Optional[str] = None
    failure_reason: Optional[str] = None
    refund_amount: Optional[float] = Field(None, ge=0)
    refund_reason: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "order_id": "507f1f77bcf86cd799439011",
                "payment_method": "credit_card",
                "payment_provider": "stripe",
                "transaction_id": "pi_1234567890abcdef",
                "status": "completed",
                "amount": 286.77,
                "currency": "USD",
                "card_last4": "4242",
                "card_brand": "Visa",
                "failure_reason": None,
                "refund_amount": None,
                "refund_reason": None,
                "metadata": {},
            }
        }

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        data.pop("_id", None)
        return data
