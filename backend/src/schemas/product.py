"""
Product API schemas for request/response validation.

These schemas define the structure of data sent to and received from
the product API endpoints.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ===== Request Schemas =====


class ProductCreateRequest(BaseModel):
    """Schema for creating a new product."""

    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    category_id: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    compare_at_price: Optional[float] = Field(None, gt=0)
    sku: str = Field(..., min_length=1, max_length=50)
    inventory_quantity: int = Field(..., ge=0)
    images: List[str] = Field(..., min_length=1, max_length=10)
    is_featured: bool = Field(default=False)
    is_active: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Wireless Bluetooth Headphones",
                "slug": "wireless-bluetooth-headphones",
                "description": "Premium noise-cancelling wireless headphones",
                "category_id": "electronics",
                "price": 129.99,
                "compare_at_price": 199.99,
                "sku": "ELEC-HEAD-001",
                "inventory_quantity": 50,
                "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"],
                "is_featured": True,
                "is_active": True
            }
        }


class ProductUpdateRequest(BaseModel):
    """Schema for updating an existing product (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)
    category_id: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    compare_at_price: Optional[float] = Field(None, gt=0)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    inventory_quantity: Optional[int] = Field(None, ge=0)
    images: Optional[List[str]] = Field(None, min_length=1, max_length=10)
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "price": 119.99,
                "inventory_quantity": 75,
                "is_featured": True
            }
        }


class ProductQueryParams(BaseModel):
    """Query parameters for listing products."""

    # Pagination
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")

    # Filters
    search: Optional[str] = Field(None, max_length=100, description="Search term")
    category_id: Optional[str] = Field(None, description="Filter by category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    is_featured: Optional[bool] = Field(None, description="Filter featured products")
    is_active: Optional[bool] = Field(default=True, description="Filter active products")
    in_stock_only: Optional[bool] = Field(None, description="Only in-stock products")

    # Sorting
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="Sort order")

    @property
    def skip(self) -> int:
        """Calculate number of documents to skip for pagination."""
        return (self.page - 1) * self.limit

    @property
    def sort_direction(self) -> int:
        """Convert sort_order to MongoDB sort direction."""
        return 1 if self.sort_order == "asc" else -1

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "limit": 20,
                "search": "headphones",
                "category_id": "electronics",
                "min_price": 50,
                "max_price": 300,
                "min_rating": 4.0,
                "in_stock_only": True,
                "sort_by": "price",
                "sort_order": "asc"
            }
        }


# ===== Response Schemas =====


class ProductResponse(BaseModel):
    """Schema for product response."""

    id: str = Field(..., alias="_id")
    name: str
    slug: str
    description: str
    category_id: str
    price: float
    compare_at_price: Optional[float] = None
    sku: str
    inventory_quantity: int
    images: List[str]
    is_featured: bool
    is_active: bool
    rating: float
    review_count: int
    created_at: datetime
    updated_at: datetime

    # Computed fields
    discount_percentage: Optional[float] = None
    is_in_stock: bool = True
    is_low_stock: bool = False

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Wireless Bluetooth Headphones",
                "slug": "wireless-bluetooth-headphones",
                "description": "Premium noise-cancelling wireless headphones",
                "category_id": "electronics",
                "price": 129.99,
                "compare_at_price": 199.99,
                "sku": "ELEC-HEAD-001",
                "inventory_quantity": 50,
                "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"],
                "is_featured": True,
                "is_active": True,
                "rating": 4.5,
                "review_count": 128,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z",
                "discount_percentage": 35.0,
                "is_in_stock": True,
                "is_low_stock": False
            }
        }


class ProductListResponse(BaseModel):
    """Schema for paginated product list response."""

    data: List[ProductResponse]
    meta: dict = Field(..., description="Pagination metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "_id": "507f1f77bcf86cd799439011",
                        "name": "Wireless Bluetooth Headphones",
                        "slug": "wireless-bluetooth-headphones",
                        "price": 129.99,
                        "rating": 4.5,
                        "review_count": 128
                    }
                ],
                "meta": {
                    "page": 1,
                    "limit": 20,
                    "total": 42,
                    "pages": 3
                }
            }
        }


class ProductDetailResponse(ProductResponse):
    """
    Extended product response with additional details.

    This schema can be extended in the future with:
    - Related products
    - Product reviews
    - Variant information
    - Custom attributes
    """

    # Future extensions
    # related_products: Optional[List[ProductResponse]] = None
    # reviews: Optional[List[ReviewResponse]] = None
    # variants: Optional[List[ProductVariant]] = None

    pass
