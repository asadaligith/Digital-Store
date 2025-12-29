"""
Checkout API routes.

Endpoints for checkout operations:
- POST /api/checkout/validate - Validate cart for checkout
- GET /api/checkout/shipping-methods - Get available shipping methods
- POST /api/checkout/calculate-shipping - Calculate shipping cost
- POST /api/checkout/preview - Create order preview
"""

from fastapi import APIRouter, Depends

from src.db.mongodb import get_database
from src.repositories.checkout_repository import CheckoutRepository
from src.repositories.cart_repository import CartRepository
from src.services.checkout_service import CheckoutService
from src.models.address import Address
from src.models.checkout import ShippingMethodType
from src.schemas.checkout import (
    ValidateCartRequest,
    CartValidationResponse,
    ShippingMethodsResponse,
    CalculateShippingRequest,
    CreateOrderPreviewRequest,
    OrderPreviewResponse,
)

router = APIRouter()


# ===== Dependencies =====


def get_checkout_service(db=Depends(get_database)) -> CheckoutService:
    """Get checkout service instance with dependencies."""
    checkout_repo = CheckoutRepository(db)
    cart_repo = CartRepository(db)
    return CheckoutService(checkout_repo, cart_repo)


# ===== Routes =====


@router.post("/validate", response_model=CartValidationResponse)
async def validate_cart(
    data: ValidateCartRequest,
    service: CheckoutService = Depends(get_checkout_service)
):
    """
    Validate cart for checkout.

    Checks:
    - Cart exists and has items
    - All products are in stock
    - Requested quantities are available

    Returns:
        Validation result with any errors or warnings
    """
    result = await service.validate_cart(data.cart_id)
    return result


@router.get("/shipping-methods", response_model=ShippingMethodsResponse)
async def get_shipping_methods(
    service: CheckoutService = Depends(get_checkout_service)
):
    """
    Get available shipping methods.

    Returns:
        List of shipping methods with costs and delivery estimates
    """
    methods = await service.get_shipping_methods()
    return {"methods": methods}


@router.post("/calculate-shipping", response_model=dict)
async def calculate_shipping(
    data: CalculateShippingRequest,
    service: CheckoutService = Depends(get_checkout_service)
):
    """
    Calculate shipping cost for selected method and destination.

    Request Body:
        - cart_id: Cart ID
        - shipping_method: Shipping method type (standard/express/overnight)
        - postal_code: Destination postal code
        - country: Destination country code

    Returns:
        Shipping method with calculated cost
    """
    method = await service.calculate_shipping_cost(
        method_type=data.shipping_method,
        postal_code=data.postal_code,
        country=data.country,
    )

    return method.model_dump()


@router.post("/preview", response_model=OrderPreviewResponse)
async def create_order_preview(
    data: CreateOrderPreviewRequest,
    service: CheckoutService = Depends(get_checkout_service)
):
    """
    Create order preview for checkout review.

    Calculates all totals (subtotal, shipping, tax, total) and
    validates cart items are available.

    Request Body:
        - cart_id: Cart ID
        - shipping_address: Complete shipping address
        - shipping_method: Selected shipping method

    Returns:
        Order preview with totals breakdown and validation status

    Raises:
        404: If cart not found
        422: If cart validation fails
    """
    # Convert address request to Address model
    address = Address(**data.shipping_address.model_dump())

    # Create order preview
    preview = await service.create_order_preview(
        cart_id=data.cart_id,
        shipping_address=address,
        shipping_method_type=data.shipping_method,
    )

    return {"preview": preview}
