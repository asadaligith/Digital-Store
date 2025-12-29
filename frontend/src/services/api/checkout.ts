/**
 * Checkout API service
 *
 * Handles all checkout-related API requests.
 */

import { apiClient } from './client';
import {
  Address,
  ShippingMethod,
  ShippingMethodType,
  OrderPreview,
  CartValidation,
} from '../../types/address';

// ===== API Functions =====

/**
 * Validate cart for checkout
 */
export const validateCart = async (cartId: string): Promise<CartValidation> => {
  const response = await apiClient.post<CartValidation>('/checkout/validate', {
    cart_id: cartId,
  });
  return response.data;
};

/**
 * Get available shipping methods
 */
export const getShippingMethods = async (): Promise<ShippingMethod[]> => {
  const response = await apiClient.get<{ methods: ShippingMethod[] }>(
    '/checkout/shipping-methods'
  );
  return response.data.methods;
};

/**
 * Calculate shipping cost for selected method
 */
export const calculateShipping = async (
  cartId: string,
  shippingMethod: ShippingMethodType,
  postalCode: string,
  country: string = 'US'
): Promise<ShippingMethod> => {
  const response = await apiClient.post<ShippingMethod>('/checkout/calculate-shipping', {
    cart_id: cartId,
    shipping_method: shippingMethod,
    postal_code: postalCode,
    country,
  });
  return response.data;
};

/**
 * Create order preview with full calculations
 */
export const createOrderPreview = async (
  cartId: string,
  shippingAddress: Omit<Address, '_id' | 'user_id'>,
  shippingMethod: ShippingMethodType
): Promise<OrderPreview> => {
  const response = await apiClient.post<{ preview: OrderPreview }>('/checkout/preview', {
    cart_id: cartId,
    shipping_address: shippingAddress,
    shipping_method: shippingMethod,
  });
  return response.data.preview;
};
