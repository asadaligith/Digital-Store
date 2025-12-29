"""
Checkout repository for database operations.

Handles checkout-related database queries including:
- Cart validation
- Shipping methods
- Stock verification
"""

from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models.checkout import ShippingMethod, SHIPPING_METHODS


class CheckoutRepository:
    """Repository for checkout database operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize checkout repository.

        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.carts = db.carts
        self.products = db.products

    async def validate_cart_items_stock(self, cart_id: str) -> tuple[bool, List[str]]:
        """
        Validate that all cart items are in stock.

        Args:
            cart_id: Cart ID to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        from bson import ObjectId

        if not ObjectId.is_valid(cart_id):
            return False, ["Invalid cart ID"]

        # Get cart
        cart = await self.carts.find_one({"_id": ObjectId(cart_id)})
        if not cart:
            return False, ["Cart not found"]

        if not cart.get("items"):
            return False, ["Cart is empty"]

        errors = []
        warnings = []

        # Validate each item
        for item in cart["items"]:
            product_id = item["product_id"]

            # Get product
            if not ObjectId.is_valid(product_id):
                errors.append(f"Invalid product ID: {product_id}")
                continue

            product = await self.products.find_one({"_id": ObjectId(product_id)})

            if not product:
                errors.append(f"Product not found: {product_id}")
                continue

            # Check stock
            inventory = product.get("inventory_quantity", 0)
            quantity = item["quantity"]

            if inventory <= 0:
                errors.append(
                    f"Product '{product.get('name', 'Unknown')}' is out of stock"
                )
            elif quantity > inventory:
                errors.append(
                    f"Product '{product.get('name', 'Unknown')}' has insufficient stock. "
                    f"Requested: {quantity}, Available: {inventory}"
                )
            elif inventory < 10:
                warnings.append(
                    f"Product '{product.get('name', 'Unknown')}' has limited stock ({inventory} remaining)"
                )

        is_valid = len(errors) == 0
        return is_valid, errors if errors else warnings

    async def get_shipping_methods(self) -> List[ShippingMethod]:
        """
        Get available shipping methods.

        Returns:
            List of available shipping methods
        """
        # In a real app, this might come from a database
        # or be calculated based on destination, weight, etc.
        return SHIPPING_METHODS

    async def get_shipping_method(self, method_type: str) -> Optional[ShippingMethod]:
        """
        Get a specific shipping method by type.

        Args:
            method_type: Shipping method type (standard/express/overnight)

        Returns:
            ShippingMethod or None if not found
        """
        for method in SHIPPING_METHODS:
            if method.method == method_type:
                return method
        return None
