"""
Product model for MongoDB.

Represents a product in the e-commerce store with:
- Basic information (name, description, price)
- Category association
- Inventory management
- Images and media
- Ratings and reviews
- SEO fields (slug, meta)
- Timestamps
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    """
    Product model representing an item for sale.

    Attributes:
        id: Unique product identifier (MongoDB ObjectId as string)
        name: Product name
        slug: URL-friendly identifier
        description: Product description
        category_id: Reference to category
        price: Current selling price
        compare_at_price: Original price (for showing discounts)
        sku: Stock Keeping Unit (unique identifier)
        inventory_quantity: Current stock level
        images: List of image URLs
        is_featured: Whether product is featured
        is_active: Whether product is available for purchase
        rating: Average customer rating (0-5)
        review_count: Number of reviews
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    category_id: str = Field(..., min_length=1)

    # Pricing
    price: float = Field(..., gt=0, description="Current selling price in USD")
    compare_at_price: Optional[float] = Field(None, gt=0, description="Original price for showing discounts")

    # Inventory
    sku: str = Field(..., min_length=1, max_length=50, description="Stock Keeping Unit")
    inventory_quantity: int = Field(..., ge=0, description="Current stock level")

    # Media
    images: List[str] = Field(default_factory=list, max_length=10)

    # Flags
    is_featured: bool = Field(default=False, description="Show on homepage/featured sections")
    is_active: bool = Field(default=True, description="Available for purchase")

    # Reviews
    rating: float = Field(default=0.0, ge=0, le=5, description="Average rating (0-5)")
    review_count: int = Field(default=0, ge=0, description="Total number of reviews")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Wireless Bluetooth Headphones",
                "slug": "wireless-bluetooth-headphones",
                "description": "Premium noise-cancelling wireless headphones with 30-hour battery life.",
                "category_id": "electronics",
                "price": 129.99,
                "compare_at_price": 199.99,
                "sku": "ELEC-HEAD-001",
                "inventory_quantity": 50,
                "images": [
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"
                ],
                "is_featured": True,
                "is_active": True,
                "rating": 4.5,
                "review_count": 128
            }
        }

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Ensure slug is URL-friendly."""
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Slug must contain only alphanumeric characters, hyphens, and underscores")
        return v.lower()

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """Ensure SKU is uppercase."""
        return v.upper()

    @field_validator("images")
    @classmethod
    def validate_images(cls, v: List[str]) -> List[str]:
        """Ensure at least one image is provided."""
        if not v:
            raise ValueError("At least one product image is required")
        return v

    @field_validator("compare_at_price")
    @classmethod
    def validate_compare_at_price(cls, v: Optional[float], info) -> Optional[float]:
        """Ensure compare_at_price is greater than price if provided."""
        if v is not None and "price" in info.data:
            price = info.data["price"]
            if v <= price:
                raise ValueError("compare_at_price must be greater than price")
        return v

    @property
    def discount_percentage(self) -> Optional[float]:
        """Calculate discount percentage if compare_at_price is set."""
        if self.compare_at_price and self.compare_at_price > self.price:
            return round(((self.compare_at_price - self.price) / self.compare_at_price) * 100, 1)
        return None

    @property
    def is_in_stock(self) -> bool:
        """Check if product is in stock."""
        return self.inventory_quantity > 0

    @property
    def is_low_stock(self) -> bool:
        """Check if product is low in stock (less than 10 items)."""
        return 0 < self.inventory_quantity < 10

    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB insertion."""
        data = self.model_dump(by_alias=True, exclude_none=True)
        # Remove computed properties
        data.pop("_id", None)
        return data


class ProductFilter(BaseModel):
    """
    Filter parameters for product queries.

    Supports:
    - Text search
    - Category filtering
    - Price range
    - Rating filter
    - Stock status
    - Featured/active filters
    """

    search: Optional[str] = Field(None, max_length=100, description="Search term for name/description")
    category_id: Optional[str] = Field(None, description="Filter by category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    is_featured: Optional[bool] = Field(None, description="Filter featured products")
    is_active: Optional[bool] = Field(True, description="Filter active products")
    in_stock_only: Optional[bool] = Field(None, description="Only show in-stock products")

    @field_validator("max_price")
    @classmethod
    def validate_price_range(cls, v: Optional[float], info) -> Optional[float]:
        """Ensure max_price is greater than min_price if both are provided."""
        if v is not None and "min_price" in info.data and info.data["min_price"] is not None:
            if v < info.data["min_price"]:
                raise ValueError("max_price must be greater than min_price")
        return v


class ProductSort(BaseModel):
    """
    Sort parameters for product queries.

    Supported sort fields:
    - created_at (newest/oldest)
    - price (low to high / high to low)
    - name (A-Z / Z-A)
    - rating (highest/lowest)
    - popularity (review_count)
    """

    field: str = Field(default="created_at", description="Field to sort by")
    order: int = Field(default=-1, ge=-1, le=1, description="Sort order: 1 = ascending, -1 = descending")

    @field_validator("field")
    @classmethod
    def validate_sort_field(cls, v: str) -> str:
        """Ensure sort field is valid."""
        allowed_fields = ["created_at", "price", "name", "rating", "review_count"]
        if v not in allowed_fields:
            raise ValueError(f"Sort field must be one of: {', '.join(allowed_fields)}")
        return v


# Common sort presets
SORT_NEWEST = ProductSort(field="created_at", order=-1)
SORT_OLDEST = ProductSort(field="created_at", order=1)
SORT_PRICE_LOW_HIGH = ProductSort(field="price", order=1)
SORT_PRICE_HIGH_LOW = ProductSort(field="price", order=-1)
SORT_NAME_A_Z = ProductSort(field="name", order=1)
SORT_NAME_Z_A = ProductSort(field="name", order=-1)
SORT_HIGHEST_RATED = ProductSort(field="rating", order=-1)
SORT_MOST_POPULAR = ProductSort(field="review_count", order=-1)
