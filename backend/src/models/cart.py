"""
Cart model for MongoDB.

Represents a shopping cart with:
- User association (or anonymous session)
- Cart items with product references
- Quantities and pricing
- Expiration for cleanup
- Timestamps
"""

from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class CartItem(BaseModel):
    """
    Individual item in a shopping cart.

    Attributes:
        product_id: Reference to product
        quantity: Number of items
        price: Price at time of adding (for price consistency)
    """

    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, description="Number of items")
    price: float = Field(..., gt=0, description="Price at time of adding")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        """Ensure quantity is reasonable."""
        if v > 100:
            raise ValueError("Quantity cannot exceed 100 items per product")
        return v


class Cart(BaseModel):
    """
    Shopping cart model.

    Attributes:
        id: Unique cart identifier (MongoDB ObjectId as string)
        user_id: Reference to user (optional for guest carts)
        session_id: Session ID for guest carts
        items: List of cart items
        expires_at: Expiration datetime (for cleanup)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    session_id: Optional[str] = Field(None, description="Session ID for guest carts")
    items: List[CartItem] = Field(default_factory=list)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=7),
        description="Cart expiration (7 days from creation)",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "session_id": None,
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439012",
                        "quantity": 2,
                        "price": 129.99,
                    }
                ],
                "expires_at": "2024-01-22T10:00:00Z",
            }
        }

    @field_validator("items")
    @classmethod
    def validate_unique_products(cls, v: List[CartItem]) -> List[CartItem]:
        """Ensure each product appears only once in cart."""
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Each product can only appear once in cart")
        return v

    @property
    def item_count(self) -> int:
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self) -> float:
        """Calculate cart subtotal."""
        return sum(item.price * item.quantity for item in self.items)

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        data.pop("_id", None)
        return data
