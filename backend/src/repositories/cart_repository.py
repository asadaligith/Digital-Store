"""
Cart repository for database operations.

Handles all MongoDB operations for shopping carts including:
- CRUD operations
- User/session cart lookup
- Cart item management
- Cart expiration cleanup
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from src.models.cart import Cart, CartItem


class CartRepository:
    """Repository for cart database operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize cart repository.

        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.collection = db.carts

    async def create(self, cart: Cart) -> str:
        """
        Create a new cart.

        Args:
            cart: Cart model instance

        Returns:
            Created cart ID
        """
        result = await self.collection.insert_one(cart.to_dict())
        return str(result.inserted_id)

    async def find_by_id(self, cart_id: str) -> Optional[Dict]:
        """
        Find a cart by ID.

        Args:
            cart_id: Cart ID

        Returns:
            Cart document or None
        """
        if not ObjectId.is_valid(cart_id):
            return None

        cart = await self.collection.find_one({"_id": ObjectId(cart_id)})

        if cart:
            cart["_id"] = str(cart["_id"])

        return cart

    async def find_by_user_id(self, user_id: str) -> Optional[Dict]:
        """
        Find cart by user ID.

        Args:
            user_id: User ID

        Returns:
            Cart document or None
        """
        cart = await self.collection.find_one({"user_id": user_id})

        if cart:
            cart["_id"] = str(cart["_id"])

        return cart

    async def find_by_session_id(self, session_id: str) -> Optional[Dict]:
        """
        Find cart by session ID (for guest carts).

        Args:
            session_id: Session ID

        Returns:
            Cart document or None
        """
        cart = await self.collection.find_one({"session_id": session_id})

        if cart:
            cart["_id"] = str(cart["_id"])

        return cart

    async def update(self, cart_id: str, update_data: Dict) -> bool:
        """
        Update a cart.

        Args:
            cart_id: Cart ID
            update_data: Fields to update

        Returns:
            True if updated, False if not found
        """
        if not ObjectId.is_valid(cart_id):
            return False

        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(cart_id)}, {"$set": update_data}
        )

        return result.modified_count > 0

    async def delete(self, cart_id: str) -> bool:
        """
        Delete a cart.

        Args:
            cart_id: Cart ID

        Returns:
            True if deleted, False if not found
        """
        if not ObjectId.is_valid(cart_id):
            return False

        result = await self.collection.delete_one({"_id": ObjectId(cart_id)})
        return result.deleted_count > 0

    async def add_item(
        self, cart_id: str, product_id: str, quantity: int, price: float
    ) -> bool:
        """
        Add or update item in cart.

        Args:
            cart_id: Cart ID
            product_id: Product ID
            quantity: Quantity to add
            price: Product price

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(cart_id):
            return False

        # Check if item already exists
        cart = await self.find_by_id(cart_id)
        if not cart:
            return False

        # Check if product already in cart
        existing_item = None
        for item in cart.get("items", []):
            if item["product_id"] == product_id:
                existing_item = item
                break

        if existing_item:
            # Update quantity
            result = await self.collection.update_one(
                {
                    "_id": ObjectId(cart_id),
                    "items.product_id": product_id,
                },
                {
                    "$inc": {"items.$.quantity": quantity},
                    "$set": {"updated_at": datetime.utcnow()},
                },
            )
        else:
            # Add new item
            new_item = {
                "product_id": product_id,
                "quantity": quantity,
                "price": price,
            }
            result = await self.collection.update_one(
                {"_id": ObjectId(cart_id)},
                {
                    "$push": {"items": new_item},
                    "$set": {"updated_at": datetime.utcnow()},
                },
            )

        return result.modified_count > 0

    async def update_item_quantity(
        self, cart_id: str, product_id: str, quantity: int
    ) -> bool:
        """
        Update item quantity in cart.

        Args:
            cart_id: Cart ID
            product_id: Product ID
            quantity: New quantity

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(cart_id):
            return False

        if quantity == 0:
            # Remove item if quantity is 0
            return await self.remove_item(cart_id, product_id)

        result = await self.collection.update_one(
            {
                "_id": ObjectId(cart_id),
                "items.product_id": product_id,
            },
            {
                "$set": {
                    "items.$.quantity": quantity,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return result.modified_count > 0

    async def remove_item(self, cart_id: str, product_id: str) -> bool:
        """
        Remove item from cart.

        Args:
            cart_id: Cart ID
            product_id: Product ID

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(cart_id):
            return False

        result = await self.collection.update_one(
            {"_id": ObjectId(cart_id)},
            {
                "$pull": {"items": {"product_id": product_id}},
                "$set": {"updated_at": datetime.utcnow()},
            },
        )

        return result.modified_count > 0

    async def clear_cart(self, cart_id: str) -> bool:
        """
        Remove all items from cart.

        Args:
            cart_id: Cart ID

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(cart_id):
            return False

        result = await self.collection.update_one(
            {"_id": ObjectId(cart_id)},
            {
                "$set": {
                    "items": [],
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return result.modified_count > 0

    async def merge_carts(self, target_cart_id: str, source_cart_id: str) -> bool:
        """
        Merge source cart into target cart.

        Used when guest logs in and we need to merge guest cart with user cart.

        Args:
            target_cart_id: Target cart ID (user's cart)
            source_cart_id: Source cart ID (guest cart)

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(target_cart_id) or not ObjectId.is_valid(source_cart_id):
            return False

        source_cart = await self.find_by_id(source_cart_id)
        target_cart = await self.find_by_id(target_cart_id)

        if not source_cart or not target_cart:
            return False

        # Merge items from source into target
        for source_item in source_cart.get("items", []):
            await self.add_item(
                target_cart_id,
                source_item["product_id"],
                source_item["quantity"],
                source_item["price"],
            )

        # Delete source cart
        await self.delete(source_cart_id)

        return True

    async def cleanup_expired_carts(self) -> int:
        """
        Delete expired carts (for maintenance/cron job).

        Returns:
            Number of carts deleted
        """
        result = await self.collection.delete_many(
            {"expires_at": {"$lt": datetime.utcnow()}}
        )

        return result.deleted_count

    async def extend_expiration(self, cart_id: str, days: int = 7) -> bool:
        """
        Extend cart expiration.

        Args:
            cart_id: Cart ID
            days: Number of days to extend

        Returns:
            True if successful
        """
        if not ObjectId.is_valid(cart_id):
            return False

        new_expiration = datetime.utcnow() + timedelta(days=days)

        result = await self.collection.update_one(
            {"_id": ObjectId(cart_id)},
            {
                "$set": {
                    "expires_at": new_expiration,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

        return result.modified_count > 0
