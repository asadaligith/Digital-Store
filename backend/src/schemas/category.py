"""
Category API schemas for request/response validation.

These schemas define the structure of data sent to and received from
the category API endpoints.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ===== Request Schemas =====


class CategoryCreateRequest(BaseModel):
    """Schema for creating a new category."""

    id: Optional[str] = Field(None, alias="_id", description="Custom category ID (optional)")
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    image_url: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    is_active: bool = Field(default=True)

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


class CategoryUpdateRequest(BaseModel):
    """Schema for updating an existing category (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    image_url: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Updated description for electronics category",
                "is_active": True
            }
        }


# ===== Response Schemas =====


class CategoryResponse(BaseModel):
    """Schema for category response."""

    id: str = Field(..., alias="_id")
    name: str
    slug: str
    description: str
    image_url: Optional[str] = None
    icon: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

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
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        }


class CategoryWithProductCountResponse(CategoryResponse):
    """Schema for category response with product count."""

    product_count: int = Field(default=0, ge=0)

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
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "product_count": 42
            }
        }


class CategoryListResponse(BaseModel):
    """Schema for category list response."""

    data: List[CategoryWithProductCountResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "_id": "electronics",
                        "name": "Electronics",
                        "slug": "electronics",
                        "description": "Latest gadgets and electronic devices",
                        "product_count": 42,
                        "is_active": True
                    },
                    {
                        "_id": "clothing",
                        "name": "Clothing",
                        "slug": "clothing",
                        "description": "Fashion and apparel for everyone",
                        "product_count": 28,
                        "is_active": True
                    }
                ]
            }
        }
