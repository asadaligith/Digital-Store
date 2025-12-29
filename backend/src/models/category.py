"""
Category model for MongoDB.

Represents a product category with:
- Basic information (name, description)
- SEO fields (slug)
- Image/icon
- Active status
- Timestamps
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Category(BaseModel):
    """
    Category model for organizing products.

    Attributes:
        id: Unique category identifier (MongoDB ObjectId as string or custom ID)
        name: Category name
        slug: URL-friendly identifier
        description: Category description
        image_url: Category image/banner URL
        icon: Icon identifier or URL
        is_active: Whether category is visible
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    image_url: Optional[str] = Field(None, description="Category banner/image URL")
    icon: Optional[str] = Field(None, max_length=100, description="Icon identifier or URL")
    is_active: bool = Field(default=True, description="Whether category is visible")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "electronics",
                "name": "Electronics",
                "slug": "electronics",
                "description": "Latest gadgets and electronic devices",
                "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800",
                "is_active": True
            }
        }

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Ensure slug is URL-friendly."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        # Keep custom _id if provided
        if self.id:
            data["_id"] = self.id
        else:
            data.pop("_id", None)
        return data


class CategoryWithProductCount(Category):
    """
    Category model extended with product count.

    Used for API responses that need to show the number of products
    in each category.
    """

    product_count: int = Field(default=0, ge=0, description="Number of products in category")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "electronics",
                "name": "Electronics",
                "slug": "electronics",
                "description": "Latest gadgets and electronic devices",
                "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800",
                "is_active": True,
                "product_count": 42
            }
        }
