/**
 * Cart API service
 *
 * Handles all cart-related API requests.
 */

import { apiClient } from './client';

// ===== Types =====

export interface CartItem {
  product_id: string;
  quantity: number;
  price: number;
  product_name?: string;
  product_slug?: string;
  product_image?: string;
  product_in_stock?: boolean;
  product_inventory?: number;
  item_total: number;
}

export interface Cart {
  _id: string;
  user_id?: string;
  session_id?: string;
  items: CartItem[];
  expires_at: string;
  created_at: string;
  updated_at: string;
  item_count: number;
  subtotal: number;
}

export interface CartSummary {
  item_count: number;
  subtotal: number;
}

export interface AddToCartRequest {
  product_id: string;
  quantity?: number;
}

export interface UpdateCartItemRequest {
  quantity: number;
}

export interface MergeCartRequest {
  session_id: string;
}

// ===== API Functions =====

/**
 * Get current user's cart
 */
export const getCart = async (): Promise<Cart> => {
  const response = await apiClient.get<Cart>('/cart');
  return response.data;
};

/**
 * Get cart summary (for header badge)
 */
export const getCartSummary = async (): Promise<CartSummary> => {
  const response = await apiClient.get<CartSummary>('/cart/summary');
  return response.data;
};

/**
 * Add item to cart
 */
export const addToCart = async (data: AddToCartRequest): Promise<Cart> => {
  const response = await apiClient.post<Cart>('/cart/items', data);
  return response.data;
};

/**
 * Update cart item quantity
 */
export const updateCartItem = async (
  productId: string,
  data: UpdateCartItemRequest
): Promise<Cart> => {
  const response = await apiClient.patch<Cart>(`/cart/items/${productId}`, data);
  return response.data;
};

/**
 * Remove item from cart
 */
export const removeFromCart = async (productId: string): Promise<Cart> => {
  const response = await apiClient.delete<Cart>(`/cart/items/${productId}`);
  return response.data;
};

/**
 * Clear all items from cart
 */
export const clearCart = async (): Promise<Cart> => {
  const response = await apiClient.delete<Cart>('/cart');
  return response.data;
};

/**
 * Merge guest cart into user cart on login
 */
export const mergeGuestCart = async (data: MergeCartRequest): Promise<Cart> => {
  const response = await apiClient.post<Cart>('/cart/merge', data);
  return response.data;
};
