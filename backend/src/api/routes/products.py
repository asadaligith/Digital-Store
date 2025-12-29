"""
Product API routes.

Provides endpoints for:
- Listing products with filtering and pagination
- Getting product details
- Creating/updating/deleting products (admin only)
- Featured products
- Products by category
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongodb import get_database
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository
from src.services.product_service import ProductService
from src.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductQueryParams,
    ProductResponse,
    ProductListResponse,
    ProductDetailResponse,
)
from src.api.dependencies.auth import get_current_user, require_roles

router = APIRouter()


# ===== Dependency Injection =====


def get_product_service(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> ProductService:
    """Get product service with injected dependencies."""
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    return ProductService(product_repo, category_repo)


# ===== Public Routes =====


@router.get(
    "",
    response_model=ProductListResponse,
    summary="List products",
    description="Get a paginated list of products with filtering and sorting options",
)
async def list_products(
    service: Annotated[ProductService, Depends(get_product_service)],
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, max_length=100, description="Search term"),
    category_id: str | None = Query(None, description="Filter by category"),
    min_price: float | None = Query(None, ge=0, description="Minimum price"),
    max_price: float | None = Query(None, ge=0, description="Maximum price"),
    min_rating: float | None = Query(None, ge=0, le=5, description="Minimum rating"),
    is_featured: bool | None = Query(None, description="Filter featured products"),
    in_stock_only: bool | None = Query(None, description="Only in-stock products"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
):
    """
    List products with filtering, sorting, and pagination.

    - **page**: Page number (starts at 1)
    - **limit**: Number of items per page (max 100)
    - **search**: Search in product name and description
    - **category_id**: Filter by category
    - **min_price** / **max_price**: Price range filter
    - **min_rating**: Minimum rating filter
    - **is_featured**: Show only featured products
    - **in_stock_only**: Show only in-stock products
    - **sort_by**: Field to sort by (created_at, price, name, rating, review_count)
    - **sort_order**: asc or desc
    """
    # Build query params
    query_params = ProductQueryParams(
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        is_featured=is_featured,
        in_stock_only=in_stock_only,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    products, meta = await service.list_products(query_params)

    return {"data": products, "meta": meta}


@router.get(
    "/featured",
    response_model=ProductListResponse,
    summary="Get featured products",
    description="Get a list of featured products for the homepage",
)
async def get_featured_products(
    service: Annotated[ProductService, Depends(get_product_service)],
    limit: int = Query(8, ge=1, le=50, description="Number of products to return"),
):
    """
    Get featured products for homepage/promotional sections.

    - **limit**: Maximum number of products (default 8, max 50)
    """
    products = await service.get_featured_products(limit)

    return {
        "data": products,
        "meta": {
            "page": 1,
            "limit": limit,
            "total": len(products),
            "pages": 1,
        },
    }


@router.get(
    "/category/{category_id}",
    response_model=ProductListResponse,
    summary="Get products by category",
    description="Get all products in a specific category with pagination",
)
async def get_products_by_category(
    category_id: str,
    service: Annotated[ProductService, Depends(get_product_service)],
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    Get products by category.

    - **category_id**: Category identifier
    - **page**: Page number
    - **limit**: Items per page
    """
    products, meta = await service.get_products_by_category(category_id, page, limit)

    return {"data": products, "meta": meta}


@router.get(
    "/{product_id}",
    response_model=ProductDetailResponse,
    summary="Get product by ID",
    description="Get detailed information about a specific product",
)
async def get_product(
    product_id: str,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    """
    Get product details by ID.

    - **product_id**: Product identifier
    """
    return await service.get_product_by_id(product_id)


@router.get(
    "/slug/{slug}",
    response_model=ProductDetailResponse,
    summary="Get product by slug",
    description="Get detailed information about a product by its URL slug",
)
async def get_product_by_slug(
    slug: str,
    service: Annotated[ProductService, Depends(get_product_service)],
):
    """
    Get product details by slug (URL-friendly identifier).

    - **slug**: Product slug (e.g., "wireless-bluetooth-headphones")
    """
    return await service.get_product_by_slug(slug)


# ===== Admin Routes (Authentication Required) =====


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new product (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def create_product(
    data: ProductCreateRequest,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Create a new product. Requires admin role.

    - **name**: Product name
    - **slug**: URL-friendly identifier
    - **description**: Product description
    - **category_id**: Category identifier
    - **price**: Current selling price
    - **sku**: Stock Keeping Unit
    - **inventory_quantity**: Stock level
    - **images**: List of image URLs
    """
    return await service.create_product(data)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description="Update an existing product (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def update_product(
    product_id: str,
    data: ProductUpdateRequest,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Update a product. Requires admin role.

    - **product_id**: Product identifier
    - All fields are optional; only provided fields will be updated
    """
    return await service.update_product(product_id, data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def delete_product(
    product_id: str,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Delete a product. Requires admin role.

    - **product_id**: Product identifier
    """
    await service.delete_product(product_id)
    return None


@router.patch(
    "/{product_id}/inventory",
    response_model=ProductResponse,
    summary="Update product inventory",
    description="Update product inventory quantity (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def update_product_inventory(
    product_id: str,
    quantity_change: int = Query(..., description="Amount to add (positive) or subtract (negative)"),
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Update product inventory.

    - **product_id**: Product identifier
    - **quantity_change**: Amount to add (positive) or remove (negative)
    """
    return await service.update_inventory(product_id, quantity_change)
