"""
Category service layer for business logic.

Handles category-related business logic including:
- Validation and data transformation
- Product count aggregations
- Category management
"""

from typing import Dict, List
from src.repositories.category_repository import CategoryRepository
from src.models.category import Category
from src.schemas.category import CategoryCreateRequest, CategoryUpdateRequest
from src.core.exceptions import NotFoundException, ValidationException


class CategoryService:
    """Service for category business logic."""

    def __init__(self, category_repo: CategoryRepository):
        """
        Initialize category service.

        Args:
            category_repo: Category repository instance
        """
        self.category_repo = category_repo

    async def create_category(self, data: CategoryCreateRequest) -> Dict:
        """
        Create a new category.

        Args:
            data: Category creation data

        Returns:
            Created category document

        Raises:
            ValidationException: If validation fails
        """
        # Create category model
        category_data = data.model_dump(by_alias=True, exclude_none=True)
        category = Category(**category_data)

        try:
            # Create in database
            category_id = await self.category_repo.create(category)

            # Fetch and return created category
            created_category = await self.category_repo.find_by_id(category_id)
            if not created_category:
                raise NotFoundException(message="Failed to fetch created category")

            return created_category

        except ValueError as e:
            raise ValidationException(message=str(e))

    async def get_category_by_id(self, category_id: str) -> Dict:
        """
        Get a category by ID.

        Args:
            category_id: Category ID

        Returns:
            Category document

        Raises:
            NotFoundException: If category not found
        """
        category = await self.category_repo.find_by_id(category_id)

        if not category:
            raise NotFoundException(message=f"Category with ID '{category_id}' not found")

        return category

    async def get_category_by_slug(self, slug: str) -> Dict:
        """
        Get a category by slug.

        Args:
            slug: Category slug

        Returns:
            Category document

        Raises:
            NotFoundException: If category not found
        """
        category = await self.category_repo.find_by_slug(slug)

        if not category:
            raise NotFoundException(message=f"Category with slug '{slug}' not found")

        return category

    async def list_categories(
        self,
        is_active: bool | None = True,
        include_product_count: bool = True
    ) -> List[Dict]:
        """
        List all categories.

        Args:
            is_active: Filter by active status (None = all)
            include_product_count: Whether to include product counts

        Returns:
            List of category documents
        """
        if include_product_count:
            return await self.category_repo.find_all_with_product_count(is_active)
        else:
            return await self.category_repo.find_all(is_active)

    async def update_category(
        self,
        category_id: str,
        data: CategoryUpdateRequest
    ) -> Dict:
        """
        Update a category.

        Args:
            category_id: Category ID
            data: Update data

        Returns:
            Updated category document

        Raises:
            NotFoundException: If category not found
            ValidationException: If validation fails
        """
        # Check category exists
        existing_category = await self.category_repo.find_by_id(category_id)
        if not existing_category:
            raise NotFoundException(message=f"Category with ID '{category_id}' not found")

        # Get only non-None fields
        update_data = data.model_dump(exclude_none=True)

        if not update_data:
            raise ValidationException(message="No fields to update")

        try:
            # Update in database
            updated = await self.category_repo.update(category_id, update_data)

            if not updated:
                raise NotFoundException(message=f"Category with ID '{category_id}' not found")

            # Fetch and return updated category
            return await self.get_category_by_id(category_id)

        except ValueError as e:
            raise ValidationException(message=str(e))

    async def delete_category(self, category_id: str) -> None:
        """
        Delete a category.

        Args:
            category_id: Category ID

        Raises:
            NotFoundException: If category not found
            ValidationException: If category has associated products
        """
        try:
            deleted = await self.category_repo.delete(category_id)

            if not deleted:
                raise NotFoundException(message=f"Category with ID '{category_id}' not found")

        except ValueError as e:
            raise ValidationException(message=str(e))

    async def get_category_product_count(self, category_id: str) -> int:
        """
        Get the number of active products in a category.

        Args:
            category_id: Category ID

        Returns:
            Number of active products

        Raises:
            NotFoundException: If category not found
        """
        # Validate category exists
        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise NotFoundException(message=f"Category with ID '{category_id}' not found")

        return await self.category_repo.get_product_count(category_id)
