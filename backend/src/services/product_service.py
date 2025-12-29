"""
Product service layer for business logic.

Handles product-related business logic including:
- Validation and data transformation
- Coordination between repositories
- Complex operations (inventory management, etc.)
"""

from typing import Dict, List, Tuple
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository
from src.models.product import Product
from src.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductQueryParams,
)
from src.core.exceptions import NotFoundException, ValidationException


class ProductService:
    """Service for product business logic."""

    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository
    ):
        """
        Initialize product service.

        Args:
            product_repo: Product repository instance
            category_repo: Category repository instance
        """
        self.product_repo = product_repo
        self.category_repo = category_repo

    async def create_product(self, data: ProductCreateRequest) -> Dict:
        """
        Create a new product.

        Args:
            data: Product creation data

        Returns:
            Created product document

        Raises:
            ValidationException: If category doesn't exist or validation fails
        """
        # Validate category exists
        category = await self.category_repo.find_by_id(data.category_id)
        if not category:
            raise ValidationException(
                message=f"Category with ID '{data.category_id}' not found",
                details={"field": "category_id"}
            )

        # Create product model
        product = Product(**data.model_dump())

        try:
            # Create in database
            product_id = await self.product_repo.create(product)

            # Fetch and return created product
            created_product = await self.product_repo.find_by_id(product_id)
            if not created_product:
                raise NotFoundException(message="Failed to fetch created product")

            return created_product

        except ValueError as e:
            raise ValidationException(message=str(e))

    async def get_product_by_id(self, product_id: str) -> Dict:
        """
        Get a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product document

        Raises:
            NotFoundException: If product not found
            ValidationException: If product_id is invalid
        """
        try:
            product = await self.product_repo.find_by_id(product_id)
        except ValueError as e:
            raise ValidationException(message=str(e))

        if not product:
            raise NotFoundException(message=f"Product with ID '{product_id}' not found")

        # Add computed fields
        product["discount_percentage"] = self._calculate_discount(product)
        product["is_in_stock"] = product.get("inventory_quantity", 0) > 0
        product["is_low_stock"] = 0 < product.get("inventory_quantity", 0) < 10

        return product

    async def get_product_by_slug(self, slug: str) -> Dict:
        """
        Get a product by slug.

        Args:
            slug: Product slug

        Returns:
            Product document

        Raises:
            NotFoundException: If product not found
        """
        product = await self.product_repo.find_by_slug(slug)

        if not product:
            raise NotFoundException(message=f"Product with slug '{slug}' not found")

        # Add computed fields
        product["discount_percentage"] = self._calculate_discount(product)
        product["is_in_stock"] = product.get("inventory_quantity", 0) > 0
        product["is_low_stock"] = 0 < product.get("inventory_quantity", 0) < 10

        return product

    async def list_products(
        self,
        query_params: ProductQueryParams
    ) -> Tuple[List[Dict], Dict]:
        """
        List products with filtering, sorting, and pagination.

        Args:
            query_params: Query parameters

        Returns:
            Tuple of (products list, pagination metadata)
        """
        products, total = await self.product_repo.find_all(query_params)

        # Calculate pagination metadata
        total_pages = (total + query_params.limit - 1) // query_params.limit

        meta = {
            "page": query_params.page,
            "limit": query_params.limit,
            "total": total,
            "pages": total_pages,
        }

        return products, meta

    async def update_product(
        self,
        product_id: str,
        data: ProductUpdateRequest
    ) -> Dict:
        """
        Update a product.

        Args:
            product_id: Product ID
            data: Update data

        Returns:
            Updated product document

        Raises:
            NotFoundException: If product not found
            ValidationException: If validation fails
        """
        # Check product exists
        existing_product = await self.product_repo.find_by_id(product_id)
        if not existing_product:
            raise NotFoundException(message=f"Product with ID '{product_id}' not found")

        # Validate category if being updated
        if data.category_id:
            category = await self.category_repo.find_by_id(data.category_id)
            if not category:
                raise ValidationException(
                    message=f"Category with ID '{data.category_id}' not found",
                    details={"field": "category_id"}
                )

        # Get only non-None fields
        update_data = data.model_dump(exclude_none=True)

        if not update_data:
            raise ValidationException(message="No fields to update")

        try:
            # Update in database
            updated = await self.product_repo.update(product_id, update_data)

            if not updated:
                raise NotFoundException(message=f"Product with ID '{product_id}' not found")

            # Fetch and return updated product
            return await self.get_product_by_id(product_id)

        except ValueError as e:
            raise ValidationException(message=str(e))

    async def delete_product(self, product_id: str) -> None:
        """
        Delete a product.

        Args:
            product_id: Product ID

        Raises:
            NotFoundException: If product not found
        """
        deleted = await self.product_repo.delete(product_id)

        if not deleted:
            raise NotFoundException(message=f"Product with ID '{product_id}' not found")

    async def get_featured_products(self, limit: int = 8) -> List[Dict]:
        """
        Get featured products for homepage.

        Args:
            limit: Maximum number of products

        Returns:
            List of featured products
        """
        return await self.product_repo.get_featured_products(limit)

    async def get_products_by_category(
        self,
        category_id: str,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Dict], Dict]:
        """
        Get products by category with pagination.

        Args:
            category_id: Category ID
            page: Page number
            limit: Items per page

        Returns:
            Tuple of (products list, pagination metadata)

        Raises:
            NotFoundException: If category not found
        """
        # Validate category exists
        category = await self.category_repo.find_by_id(category_id)
        if not category:
            raise NotFoundException(message=f"Category with ID '{category_id}' not found")

        # Calculate skip
        skip = (page - 1) * limit

        # Get products
        products, total = await self.product_repo.get_products_by_category(
            category_id, limit, skip
        )

        # Calculate pagination metadata
        total_pages = (total + limit - 1) // limit

        meta = {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": total_pages,
        }

        return products, meta

    async def update_inventory(
        self,
        product_id: str,
        quantity_change: int
    ) -> Dict:
        """
        Update product inventory.

        Args:
            product_id: Product ID
            quantity_change: Amount to add (positive) or subtract (negative)

        Returns:
            Updated product document

        Raises:
            NotFoundException: If product not found
            ValidationException: If insufficient inventory
        """
        try:
            new_quantity = await self.product_repo.update_inventory(
                product_id, quantity_change
            )

            if new_quantity is None:
                raise NotFoundException(message=f"Product with ID '{product_id}' not found")

            # Return updated product
            return await self.get_product_by_id(product_id)

        except ValueError as e:
            raise ValidationException(message=str(e))

    @staticmethod
    def _calculate_discount(product: Dict) -> float | None:
        """Calculate discount percentage."""
        compare_at = product.get("compare_at_price")
        price = product.get("price")

        if compare_at and price and compare_at > price:
            return round(((compare_at - price) / compare_at) * 100, 1)

        return None
