"""
Checkout service layer for business logic.

Handles checkout-related business logic including:
- Cart validation
- Shipping cost calculation
- Tax calculation
- Order preview generation
"""

from typing import Dict, List
from src.repositories.checkout_repository import CheckoutRepository
from src.repositories.cart_repository import CartRepository
from src.models.checkout import (
    ShippingMethod,
    CheckoutTotals,
    OrderPreview,
    ShippingMethodType,
)
from src.models.address import Address
from src.core.exceptions import NotFoundException, ValidationException


class CheckoutService:
    """Service for checkout business logic."""

    # Tax rates by state (simplified - in real app, use tax API)
    TAX_RATES = {
        "NY": 0.08875,  # New York
        "CA": 0.0725,   # California
        "TX": 0.0625,   # Texas
        "FL": 0.06,     # Florida
        "IL": 0.0625,   # Illinois
        # Add more states as needed
    }

    DEFAULT_TAX_RATE = 0.08  # 8% default

    def __init__(
        self,
        checkout_repo: CheckoutRepository,
        cart_repo: CartRepository
    ):
        """
        Initialize checkout service.

        Args:
            checkout_repo: Checkout repository instance
            cart_repo: Cart repository instance
        """
        self.checkout_repo = checkout_repo
        self.cart_repo = cart_repo

    async def validate_cart(self, cart_id: str) -> Dict:
        """
        Validate cart for checkout.

        Args:
            cart_id: Cart ID to validate

        Returns:
            Validation result with status, errors, warnings

        Raises:
            NotFoundException: If cart not found
        """
        # Get cart
        cart = await self.cart_repo.find_by_id(cart_id)

        if not cart:
            raise NotFoundException(message=f"Cart with ID '{cart_id}' not found")

        # Validate items stock
        is_valid, messages = await self.checkout_repo.validate_cart_items_stock(cart_id)

        # Determine if messages are errors or warnings
        errors = messages if not is_valid else []
        warnings = messages if is_valid else []

        return {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "items_count": cart.get("item_count", 0),
            "subtotal": cart.get("subtotal", 0.0),
        }

    async def get_shipping_methods(self) -> List[ShippingMethod]:
        """
        Get available shipping methods.

        Returns:
            List of available shipping methods
        """
        return await self.checkout_repo.get_shipping_methods()

    async def calculate_shipping_cost(
        self,
        method_type: ShippingMethodType,
        postal_code: str = None,
        country: str = "US"
    ) -> ShippingMethod:
        """
        Calculate shipping cost based on method and destination.

        Args:
            method_type: Shipping method type
            postal_code: Destination postal code
            country: Destination country

        Returns:
            ShippingMethod with calculated cost

        Raises:
            ValidationException: If shipping method not found
        """
        method = await self.checkout_repo.get_shipping_method(method_type)

        if not method:
            raise ValidationException(
                message=f"Shipping method '{method_type}' not found"
            )

        # In a real app, adjust cost based on destination, weight, etc.
        # For now, return the base cost
        return method

    async def calculate_tax(
        self,
        subtotal: float,
        state: str = None,
        country: str = "US"
    ) -> float:
        """
        Calculate sales tax based on destination.

        Args:
            subtotal: Cart subtotal
            state: Destination state code
            country: Destination country code

        Returns:
            Tax amount
        """
        if country != "US":
            # For non-US, could integrate with international tax APIs
            return 0.0

        # Get tax rate for state
        tax_rate = self.TAX_RATES.get(state, self.DEFAULT_TAX_RATE)

        # Calculate tax
        tax = subtotal * tax_rate

        return round(tax, 2)

    async def create_order_preview(
        self,
        cart_id: str,
        shipping_address: Address,
        shipping_method_type: ShippingMethodType
    ) -> OrderPreview:
        """
        Create order preview for checkout review.

        Args:
            cart_id: Cart ID
            shipping_address: Shipping address
            shipping_method_type: Selected shipping method

        Returns:
            OrderPreview with all totals calculated

        Raises:
            NotFoundException: If cart not found
            ValidationException: If cart validation fails
        """
        # Validate cart
        validation = await self.validate_cart(cart_id)

        if not validation["valid"]:
            return OrderPreview(
                cart_id=cart_id,
                items_count=validation["items_count"],
                totals=CheckoutTotals(
                    subtotal=validation["subtotal"],
                    shipping=0.0,
                    tax=0.0,
                    total=validation["subtotal"],
                ),
                can_proceed=False,
                validation_errors=validation["errors"],
            )

        # Get shipping method
        shipping_method = await self.calculate_shipping_cost(
            method_type=shipping_method_type,
            postal_code=shipping_address.postal_code,
            country=shipping_address.country,
        )

        # Calculate tax
        subtotal = validation["subtotal"]
        tax = await self.calculate_tax(
            subtotal=subtotal,
            state=shipping_address.state,
            country=shipping_address.country,
        )

        # Calculate total
        total = subtotal + shipping_method.cost + tax

        # Create totals
        totals = CheckoutTotals(
            subtotal=subtotal,
            shipping=shipping_method.cost,
            tax=tax,
            discount=0.0,
            total=round(total, 2),
        )

        # Create order preview
        preview = OrderPreview(
            cart_id=cart_id,
            items_count=validation["items_count"],
            totals=totals,
            shipping_address=shipping_address.model_dump(exclude={"id", "user_id", "created_at", "updated_at"}),
            shipping_method=shipping_method,
            can_proceed=True,
            validation_errors=[],
        )

        return preview
