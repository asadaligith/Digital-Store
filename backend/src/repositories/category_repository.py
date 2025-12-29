"""
Category repository for database operations.

Handles all MongoDB operations for categories including:
- CRUD operations
- Product count aggregations
- Active category filtering
"""

from typing import Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models.category import Category


class CategoryRepository:
    """Repository for category database operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize category repository.

        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.collection = db.categories
        self.products_collection = db.products

    async def create(self, category: Category) -> str:
        """
        Create a new category.

        Args:
            category: Category model instance

        Returns:
            Created category ID

        Raises:
            ValueError: If slug already exists
        """
        # Check for duplicate slug
        existing = await self.collection.find_one({"slug": category.slug})
        if existing:
            raise ValueError(f"Category with slug '{category.slug}' already exists")

        # Insert category
        category_dict = category.to_dict()
        result = await self.collection.insert_one(category_dict)

        # Return custom ID if provided, otherwise MongoDB generated ID
        return category.id if category.id else str(result.inserted_id)

    async def find_by_id(self, category_id: str) -> Optional[Dict]:
        """
        Find a category by ID.

        Args:
            category_id: Category ID (can be custom ID or ObjectId)

        Returns:
            Category document or None
        """
        # Try finding by custom _id first (string)
        category = await self.collection.find_one({"_id": category_id})

        if category:
            # Ensure _id is string
            category["_id"] = str(category["_id"])

        return category

    async def find_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Find a category by slug.

        Args:
            slug: Category slug

        Returns:
            Category document or None
        """
        category = await self.collection.find_one({"slug": slug})

        if category:
            category["_id"] = str(category["_id"])

        return category

    async def find_all(self, is_active: Optional[bool] = None) -> List[Dict]:
        """
        Find all categories.

        Args:
            is_active: Filter by active status (None = all categories)

        Returns:
            List of category documents
        """
        query = {}
        if is_active is not None:
            query["is_active"] = is_active

        cursor = self.collection.find(query).sort("name", 1)

        categories = []
        async for category in cursor:
            category["_id"] = str(category["_id"])
            categories.append(category)

        return categories

    async def find_all_with_product_count(
        self,
        is_active: Optional[bool] = True
    ) -> List[Dict]:
        """
        Find all categories with product counts.

        Args:
            is_active: Filter by active status (None = all categories)

        Returns:
            List of category documents with product_count field
        """
        # Build match stage
        match_stage = {}
        if is_active is not None:
            match_stage["is_active"] = is_active

        # Aggregation pipeline
        pipeline = [
            {"$match": match_stage},
            {
                "$lookup": {
                    "from": "products",
                    "let": {"category_id": {"$toString": "$_id"}},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$category_id", "$$category_id"]},
                                        {"$eq": ["$is_active", True]}
                                    ]
                                }
                            }
                        },
                        {"$count": "count"}
                    ],
                    "as": "product_data"
                }
            },
            {
                "$addFields": {
                    "product_count": {
                        "$ifNull": [
                            {"$arrayElemAt": ["$product_data.count", 0]},
                            0
                        ]
                    }
                }
            },
            {"$project": {"product_data": 0}},
            {"$sort": {"name": 1}}
        ]

        cursor = self.collection.aggregate(pipeline)

        categories = []
        async for category in cursor:
            category["_id"] = str(category["_id"])
            categories.append(category)

        return categories

    async def update(self, category_id: str, update_data: Dict) -> bool:
        """
        Update a category.

        Args:
            category_id: Category ID
            update_data: Fields to update

        Returns:
            True if updated, False if not found

        Raises:
            ValueError: If slug already exists
        """
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Check for duplicate slug if slug is being updated
        if "slug" in update_data:
            existing = await self.collection.find_one({
                "slug": update_data["slug"],
                "_id": {"$ne": category_id}
            })
            if existing:
                raise ValueError(f"Category with slug '{update_data['slug']}' already exists")

        result = await self.collection.update_one(
            {"_id": category_id},
            {"$set": update_data}
        )

        return result.modified_count > 0

    async def delete(self, category_id: str) -> bool:
        """
        Delete a category.

        Note: This does NOT delete associated products. Consider implementing
        a cascading delete or reassigning products in a production system.

        Args:
            category_id: Category ID

        Returns:
            True if deleted, False if not found
        """
        # Check if category has products
        product_count = await self.products_collection.count_documents({
            "category_id": category_id
        })

        if product_count > 0:
            raise ValueError(
                f"Cannot delete category with {product_count} associated products. "
                "Please reassign or delete products first."
            )

        result = await self.collection.delete_one({"_id": category_id})
        return result.deleted_count > 0

    async def get_product_count(self, category_id: str) -> int:
        """
        Get the number of active products in a category.

        Args:
            category_id: Category ID

        Returns:
            Number of active products
        """
        count = await self.products_collection.count_documents({
            "category_id": category_id,
            "is_active": True
        })

        return count
