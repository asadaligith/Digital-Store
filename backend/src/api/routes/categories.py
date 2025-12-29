"""
Category API routes.

Provides endpoints for:
- Listing categories
- Getting category details
- Creating/updating/deleting categories (admin only)
- Category product counts
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.db.mongodb import get_database
from src.repositories.category_repository import CategoryRepository
from src.services.category_service import CategoryService
from src.schemas.category import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategoryListResponse,
    CategoryWithProductCountResponse,
)
from src.api.dependencies.auth import get_current_user, require_roles

router = APIRouter()


# ===== Dependency Injection =====


def get_category_service(db: Annotated[AsyncIOMotorDatabase, Depends(get_database)]) -> CategoryService:
    """Get category service with injected dependencies."""
    category_repo = CategoryRepository(db)
    return CategoryService(category_repo)


# ===== Public Routes =====


@router.get(
    "",
    response_model=CategoryListResponse,
    summary="List categories",
    description="Get all categories with product counts",
)
async def list_categories(
    service: Annotated[CategoryService, Depends(get_category_service)],
    is_active: bool | None = Query(True, description="Filter by active status"),
    include_product_count: bool = Query(True, description="Include product counts"),
):
    """
    List all categories.

    - **is_active**: Filter by active status (null = all categories)
    - **include_product_count**: Whether to include product counts (default: true)
    """
    categories = await service.list_categories(is_active, include_product_count)

    return {"data": categories}


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get category by ID",
    description="Get detailed information about a specific category",
)
async def get_category(
    category_id: str,
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    """
    Get category details by ID.

    - **category_id**: Category identifier
    """
    return await service.get_category_by_id(category_id)


@router.get(
    "/slug/{slug}",
    response_model=CategoryResponse,
    summary="Get category by slug",
    description="Get detailed information about a category by its URL slug",
)
async def get_category_by_slug(
    slug: str,
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    """
    Get category details by slug (URL-friendly identifier).

    - **slug**: Category slug (e.g., "electronics")
    """
    return await service.get_category_by_slug(slug)


@router.get(
    "/{category_id}/product-count",
    summary="Get category product count",
    description="Get the number of active products in a category",
)
async def get_category_product_count(
    category_id: str,
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    """
    Get the number of active products in a category.

    - **category_id**: Category identifier
    """
    count = await service.get_category_product_count(category_id)

    return {"category_id": category_id, "product_count": count}


# ===== Admin Routes (Authentication Required) =====


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
    description="Create a new category (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def create_category(
    data: CategoryCreateRequest,
    service: Annotated[CategoryService, Depends(get_category_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Create a new category. Requires admin role.

    - **name**: Category name
    - **slug**: URL-friendly identifier
    - **description**: Category description
    - **image_url**: Category banner/image URL (optional)
    - **icon**: Icon identifier or URL (optional)
    """
    return await service.create_category(data)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update category",
    description="Update an existing category (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def update_category(
    category_id: str,
    data: CategoryUpdateRequest,
    service: Annotated[CategoryService, Depends(get_category_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Update a category. Requires admin role.

    - **category_id**: Category identifier
    - All fields are optional; only provided fields will be updated
    """
    return await service.update_category(category_id, data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
    description="Delete a category (admin only)",
    dependencies=[Depends(require_roles(["admin"]))],
)
async def delete_category(
    category_id: str,
    service: Annotated[CategoryService, Depends(get_category_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Delete a category. Requires admin role.

    Note: Categories with products cannot be deleted.

    - **category_id**: Category identifier
    """
    await service.delete_category(category_id)
    return None
