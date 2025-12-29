"""
Product repository for database operations.

Handles all MongoDB operations for products including:
- CRUD operations
- Search and filtering
- Pagination
- Aggregations
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from src.models.product import Product, ProductFilter, ProductSort
from src.schemas.product import ProductQueryParams, ProductResponse
from src.core.exceptions import NotFoundException


class ProductRepository:
    """Repository for product database operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize product repository.

        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.collection = db.products

    async def create(self, product: Product) -> str:
        """
        Create a new product.

        Args:
            product: Product model instance

        Returns:
            Created product ID

        Raises:
            Exception: If SKU or slug already exists
        """
        # Check for duplicate SKU
        existing_sku = await self.collection.find_one({"sku": product.sku})
        if existing_sku:
            raise ValueError(f"Product with SKU '{product.sku}' already exists")

        # Check for duplicate slug
        existing_slug = await self.collection.find_one({"slug": product.slug})
        if existing_slug:
            raise ValueError(f"Product with slug '{product.slug}' already exists")

        # Insert product
        result = await self.collection.insert_one(product.to_dict())
        return str(result.inserted_id)

    async def find_by_id(self, product_id: str) -> Optional[Dict]:
        """
        Find a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product document or None

        Raises:
            ValueError: If product_id is not a valid ObjectId
        """
        if not ObjectId.is_valid(product_id):
            raise ValueError(f"Invalid product ID: {product_id}")

        product = await self.collection.find_one({"_id": ObjectId(product_id)})

        if product:
            # Convert ObjectId to string for JSON serialization
            product["_id"] = str(product["_id"])

        return product

    async def find_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Find a product by slug.

        Args:
            slug: Product slug

        Returns:
            Product document or None
        """
        product = await self.collection.find_one({"slug": slug})

        if product:
            product["_id"] = str(product["_id"])

        return product

    async def find_all(
        self,
        query_params: ProductQueryParams
    ) -> Tuple[List[Dict], int]:
        """
        Find all products with filtering, sorting, and pagination.

        Args:
            query_params: Query parameters for filtering and pagination

        Returns:
            Tuple of (products list, total count)
        """
        # Build filter query
        filter_query = self._build_filter_query(query_params)

        # Get total count
        total = await self.collection.count_documents(filter_query)

        # Build sort
        sort = [(query_params.sort_by, query_params.sort_direction)]

        # Execute query with pagination
        cursor = self.collection.find(filter_query).sort(sort).skip(query_params.skip).limit(query_params.limit)

        products = []
        async for product in cursor:
            product["_id"] = str(product["_id"])
            # Add computed fields
            product["discount_percentage"] = self._calculate_discount(product)
            product["is_in_stock"] = product.get("inventory_quantity", 0) > 0
            product["is_low_stock"] = 0 < product.get("inventory_quantity", 0) < 10
            products.append(product)

        return products, total

    async def update(self, product_id: str, update_data: Dict) -> bool:
        """
        Update a product.

        Args:
            product_id: Product ID
            update_data: Fields to update

        Returns:
            True if updated, False if not found

        Raises:
            ValueError: If product_id is not valid
        """
        if not ObjectId.is_valid(product_id):
            raise ValueError(f"Invalid product ID: {product_id}")

        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Check for duplicate slug if slug is being updated
        if "slug" in update_data:
            existing = await self.collection.find_one({
                "slug": update_data["slug"],
                "_id": {"$ne": ObjectId(product_id)}
            })
            if existing:
                raise ValueError(f"Product with slug '{update_data['slug']}' already exists")

        # Check for duplicate SKU if SKU is being updated
        if "sku" in update_data:
            existing = await self.collection.find_one({
                "sku": update_data["sku"],
                "_id": {"$ne": ObjectId(product_id)}
            })
            if existing:
                raise ValueError(f"Product with SKU '{update_data['sku']}' already exists")

        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )

        return result.modified_count > 0

    async def delete(self, product_id: str) -> bool:
        """
        Delete a product.

        Args:
            product_id: Product ID

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If product_id is not valid
        """
        if not ObjectId.is_valid(product_id):
            raise ValueError(f"Invalid product ID: {product_id}")

        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    async def update_inventory(self, product_id: str, quantity_change: int) -> Optional[int]:
        """
        Update product inventory quantity.

        Args:
            product_id: Product ID
            quantity_change: Amount to add (positive) or subtract (negative)

        Returns:
            New inventory quantity or None if product not found

        Raises:
            ValueError: If resulting quantity would be negative
        """
        if not ObjectId.is_valid(product_id):
            raise ValueError(f"Invalid product ID: {product_id}")

        # Get current product
        product = await self.find_by_id(product_id)
        if not product:
            return None

        new_quantity = product["inventory_quantity"] + quantity_change

        if new_quantity < 0:
            raise ValueError(f"Insufficient inventory. Available: {product['inventory_quantity']}, Requested: {abs(quantity_change)}")

        # Update quantity
        await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "inventory_quantity": new_quantity,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return new_quantity

    async def get_featured_products(self, limit: int = 8) -> List[Dict]:
        """
        Get featured products.

        Args:
            limit: Maximum number of products to return

        Returns:
            List of featured products
        """
        cursor = self.collection.find({
            "is_featured": True,
            "is_active": True
        }).sort("created_at", -1).limit(limit)

        products = []
        async for product in cursor:
            product["_id"] = str(product["_id"])
            product["discount_percentage"] = self._calculate_discount(product)
            product["is_in_stock"] = product.get("inventory_quantity", 0) > 0
            product["is_low_stock"] = 0 < product.get("inventory_quantity", 0) < 10
            products.append(product)

        return products

    async def get_products_by_category(
        self,
        category_id: str,
        limit: int = 20,
        skip: int = 0
    ) -> Tuple[List[Dict], int]:
        """
        Get products by category with pagination.

        Args:
            category_id: Category ID
            limit: Maximum number of products
            skip: Number of products to skip

        Returns:
            Tuple of (products list, total count)
        """
        filter_query = {"category_id": category_id, "is_active": True}

        total = await self.collection.count_documents(filter_query)

        cursor = self.collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)

        products = []
        async for product in cursor:
            product["_id"] = str(product["_id"])
            product["discount_percentage"] = self._calculate_discount(product)
            product["is_in_stock"] = product.get("inventory_quantity", 0) > 0
            product["is_low_stock"] = 0 < product.get("inventory_quantity", 0) < 10
            products.append(product)

        return products, total

    def _build_filter_query(self, params: ProductQueryParams) -> Dict:
        """Build MongoDB filter query from query parameters."""
        query = {}

        # Active filter (always applied unless explicitly set to False)
        if params.is_active is not None:
            query["is_active"] = params.is_active

        # Text search
        if params.search:
            query["$text"] = {"$search": params.search}

        # Category filter
        if params.category_id:
            query["category_id"] = params.category_id

        # Price range
        if params.min_price is not None or params.max_price is not None:
            query["price"] = {}
            if params.min_price is not None:
                query["price"]["$gte"] = params.min_price
            if params.max_price is not None:
                query["price"]["$lte"] = params.max_price

        # Rating filter
        if params.min_rating is not None:
            query["rating"] = {"$gte": params.min_rating}

        # Featured filter
        if params.is_featured is not None:
            query["is_featured"] = params.is_featured

        # Stock filter
        if params.in_stock_only:
            query["inventory_quantity"] = {"$gt": 0}

        return query

    @staticmethod
    def _calculate_discount(product: Dict) -> Optional[float]:
        """Calculate discount percentage."""
        compare_at = product.get("compare_at_price")
        price = product.get("price")

        if compare_at and price and compare_at > price:
            return round(((compare_at - price) / compare_at) * 100, 1)

        return None
