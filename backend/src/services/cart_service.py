"""
Cart service layer for business logic.

Handles cart-related business logic including:
- Cart creation and management
- Product validation before adding to cart
- Product details population
- Cart item calculations
- Guest cart merging
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.repositories.cart_repository import CartRepository
from src.repositories.product_repository import ProductRepository
from src.models.cart import Cart, CartItem
from src.schemas.cart import AddToCartRequest, UpdateCartItemRequest
from src.core.exceptions import NotFoundException, ValidationException


class CartService:
    """Service for cart business logic."""

    def __init__(
        self,
        cart_repo: CartRepository,
        product_repo: ProductRepository
    ):
        """
        Initialize cart service.

        Args:
            cart_repo: Cart repository instance
            product_repo: Product repository instance
        """
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    async def get_or_create_cart(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Get existing cart or create new one.

        Args:
            user_id: User ID (for authenticated users)
            session_id: Session ID (for guest users)

        Returns:
            Cart document with populated product details

        Raises:
            ValidationException: If both user_id and session_id are None
        """
        if not user_id and not session_id:
            raise ValidationException(
                message="Either user_id or session_id must be provided"
            )

        # Try to find existing cart
        if user_id:
            cart = await self.cart_repo.find_by_user_id(user_id)
        else:
            cart = await self.cart_repo.find_by_session_id(session_id)

        # Create new cart if not found
        if not cart:
            new_cart = Cart(user_id=user_id, session_id=session_id)
            cart_id = await self.cart_repo.create(new_cart)
            cart = await self.cart_repo.find_by_id(cart_id)

        # Populate product details
        cart = await self._populate_cart_products(cart)

        return cart

    async def get_cart(self, cart_id: str) -> Dict:
        """
        Get cart by ID.

        Args:
            cart_id: Cart ID

        Returns:
            Cart document with populated product details

        Raises:
            NotFoundException: If cart not found
        """
        cart = await self.cart_repo.find_by_id(cart_id)

        if not cart:
            raise NotFoundException(message=f"Cart with ID '{cart_id}' not found")

        # Populate product details
        cart = await self._populate_cart_products(cart)

        return cart

    async def add_to_cart(
        self,
        cart_id: str,
        data: AddToCartRequest
    ) -> Dict:
        """
        Add item to cart.

        Args:
            cart_id: Cart ID
            data: Add to cart request data

        Returns:
            Updated cart with populated product details

        Raises:
            NotFoundException: If cart or product not found
            ValidationException: If product is out of stock or quantity exceeds inventory
        """
        # Validate product exists and is available
        product = await self.product_repo.find_by_id(data.product_id)

        if not product:
            raise NotFoundException(
                message=f"Product with ID '{data.product_id}' not found"
            )

        # Check if product is in stock
        inventory_quantity = product.get("inventory_quantity", 0)
        if inventory_quantity <= 0:
            raise ValidationException(
                message="Product is out of stock",
                details={"product_id": data.product_id}
            )

        # Check if requested quantity is available
        if data.quantity > inventory_quantity:
            raise ValidationException(
                message=f"Only {inventory_quantity} items available in stock",
                details={
                    "product_id": data.product_id,
                    "requested": data.quantity,
                    "available": inventory_quantity
                }
            )

        # Add item to cart
        success = await self.cart_repo.add_item(
            cart_id=cart_id,
            product_id=data.product_id,
            quantity=data.quantity,
            price=product["price"]
        )

        if not success:
            raise NotFoundException(message=f"Cart with ID '{cart_id}' not found")

        # Return updated cart
        return await self.get_cart(cart_id)

    async def update_cart_item(
        self,
        cart_id: str,
        product_id: str,
        data: UpdateCartItemRequest
    ) -> Dict:
        """
        Update cart item quantity.

        Args:
            cart_id: Cart ID
            product_id: Product ID
            data: Update request data

        Returns:
            Updated cart with populated product details

        Raises:
            NotFoundException: If cart or product not found
            ValidationException: If quantity exceeds inventory
        """
        # If quantity > 0, validate against inventory
        if data.quantity > 0:
            product = await self.product_repo.find_by_id(product_id)

            if not product:
                raise NotFoundException(
                    message=f"Product with ID '{product_id}' not found"
                )

            inventory_quantity = product.get("inventory_quantity", 0)
            if data.quantity > inventory_quantity:
                raise ValidationException(
                    message=f"Only {inventory_quantity} items available in stock",
                    details={
                        "product_id": product_id,
                        "requested": data.quantity,
                        "available": inventory_quantity
                    }
                )

        # Update item quantity (will remove if quantity is 0)
        success = await self.cart_repo.update_item_quantity(
            cart_id=cart_id,
            product_id=product_id,
            quantity=data.quantity
        )

        if not success:
            raise NotFoundException(
                message=f"Cart or item not found",
                details={"cart_id": cart_id, "product_id": product_id}
            )

        # Return updated cart
        return await self.get_cart(cart_id)

    async def remove_from_cart(
        self,
        cart_id: str,
        product_id: str
    ) -> Dict:
        """
        Remove item from cart.

        Args:
            cart_id: Cart ID
            product_id: Product ID to remove

        Returns:
            Updated cart with populated product details

        Raises:
            NotFoundException: If cart or item not found
        """
        success = await self.cart_repo.remove_item(cart_id, product_id)

        if not success:
            raise NotFoundException(
                message=f"Cart or item not found",
                details={"cart_id": cart_id, "product_id": product_id}
            )

        # Return updated cart
        return await self.get_cart(cart_id)

    async def clear_cart(self, cart_id: str) -> Dict:
        """
        Remove all items from cart.

        Args:
            cart_id: Cart ID

        Returns:
            Empty cart

        Raises:
            NotFoundException: If cart not found
        """
        success = await self.cart_repo.clear_cart(cart_id)

        if not success:
            raise NotFoundException(message=f"Cart with ID '{cart_id}' not found")

        # Return updated cart
        return await self.get_cart(cart_id)

    async def merge_guest_cart(
        self,
        user_id: str,
        session_id: str
    ) -> Dict:
        """
        Merge guest cart into user cart on login.

        Args:
            user_id: User ID (authenticated user)
            session_id: Session ID (guest cart)

        Returns:
            Merged user cart with populated product details

        Raises:
            NotFoundException: If guest cart not found
        """
        # Get or create user cart
        user_cart = await self.cart_repo.find_by_user_id(user_id)
        if not user_cart:
            new_cart = Cart(user_id=user_id)
            user_cart_id = await self.cart_repo.create(new_cart)
            user_cart = await self.cart_repo.find_by_id(user_cart_id)

        # Get guest cart
        guest_cart = await self.cart_repo.find_by_session_id(session_id)

        if not guest_cart:
            # No guest cart to merge, return user cart
            return await self._populate_cart_products(user_cart)

        # Merge carts
        success = await self.cart_repo.merge_carts(
            target_cart_id=user_cart["_id"],
            source_cart_id=guest_cart["_id"]
        )

        if not success:
            raise ValidationException(message="Failed to merge carts")

        # Return merged cart
        return await self.get_cart(user_cart["_id"])

    async def get_cart_summary(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Get lightweight cart summary (for header badge, etc.).

        Args:
            user_id: User ID (for authenticated users)
            session_id: Session ID (for guest users)

        Returns:
            Cart summary with item_count and subtotal
        """
        cart = await self.get_or_create_cart(user_id=user_id, session_id=session_id)

        return {
            "item_count": cart["item_count"],
            "subtotal": cart["subtotal"]
        }

    async def _populate_cart_products(self, cart: Dict) -> Dict:
        """
        Populate cart items with product details.

        Args:
            cart: Cart document

        Returns:
            Cart with populated product details in items
        """
        if not cart or not cart.get("items"):
            # Add computed fields for empty cart
            cart["item_count"] = 0
            cart["subtotal"] = 0.0
            return cart

        # Fetch all products in cart
        product_ids = [item["product_id"] for item in cart["items"]]
        products = {}

        for product_id in product_ids:
            product = await self.product_repo.find_by_id(product_id)
            if product:
                products[product_id] = product

        # Populate items with product details
        populated_items = []
        item_count = 0
        subtotal = 0.0

        for item in cart["items"]:
            product = products.get(item["product_id"])

            populated_item = {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": item["price"],
                "item_total": item["price"] * item["quantity"]
            }

            # Add product details if product exists
            if product:
                populated_item["product_name"] = product.get("name")
                populated_item["product_slug"] = product.get("slug")
                populated_item["product_image"] = (
                    product.get("images", [{}])[0].get("url") if product.get("images") else None
                )
                populated_item["product_in_stock"] = product.get("inventory_quantity", 0) > 0
                populated_item["product_inventory"] = product.get("inventory_quantity", 0)

            populated_items.append(populated_item)

            # Update totals
            item_count += item["quantity"]
            subtotal += populated_item["item_total"]

        # Update cart with populated items and computed fields
        cart["items"] = populated_items
        cart["item_count"] = item_count
        cart["subtotal"] = round(subtotal, 2)

        return cart
