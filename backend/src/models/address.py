"""
Address model for MongoDB.

Represents a shipping or billing address with:
- User association (optional for guest checkout)
- Address type (shipping/billing/both)
- Complete address information
- Contact phone number
- Default address flag
"""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import re


class AddressType(str, Enum):
    """Address type enumeration."""
    SHIPPING = "shipping"
    BILLING = "billing"
    BOTH = "both"


class Address(BaseModel):
    """
    Address model for shipping and billing.

    Attributes:
        id: Unique address identifier (MongoDB ObjectId as string)
        user_id: Reference to user (optional for guest checkout)
        type: Address type (shipping/billing/both)
        full_name: Recipient's full name
        address_line1: Primary address line
        address_line2: Secondary address line (apartment, suite, etc.)
        city: City name
        state: State/province code
        postal_code: ZIP/postal code
        country: Country code (ISO 3166-1 alpha-2)
        phone: Contact phone number
        is_default: Whether this is the default address
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
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

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)\.]', '', v)

        # Check if it contains only digits and optional + prefix
        if not re.match(r'^\+?\d{10,15}$', cleaned):
            raise ValueError("Phone number must be 10-15 digits (with optional + prefix)")

        return v

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        """Validate postal code format."""
        # Allow alphanumeric and spaces/hyphens
        if not re.match(r'^[A-Z0-9\s\-]{3,10}$', v.upper()):
            raise ValueError("Invalid postal code format")

        return v.upper()

    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str) -> str:
        """Validate country code format."""
        if not re.match(r'^[A-Z]{2}$', v.upper()):
            raise ValueError("Country must be 2-letter ISO code (e.g., US, CA, GB)")

        return v.upper()

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        """Convert state to uppercase."""
        return v.upper()

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        data.pop("_id", None)
        return data
