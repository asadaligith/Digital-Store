/**
 * Cart Context
 *
 * Provides cart state and actions to the entire application.
 * Manages cart data fetching, updates, and synchronization.
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  Cart,
  CartSummary,
  AddToCartRequest,
  getCart,
  getCartSummary,
  addToCart as addToCartAPI,
  updateCartItem as updateCartItemAPI,
  removeFromCart as removeFromCartAPI,
  clearCart as clearCartAPI,
} from '../services/api/cart';

// ===== Types =====

interface CartContextValue {
  // State
  cart: Cart | null;
  summary: CartSummary | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchCart: () => Promise<void>;
  fetchCartSummary: () => Promise<void>;
  addToCart: (data: AddToCartRequest) => Promise<void>;
  updateCartItem: (productId: string, quantity: number) => Promise<void>;
  removeFromCart: (productId: string) => Promise<void>;
  clearCart: () => Promise<void>;
  refreshCart: () => Promise<void>;
}

// ===== Context =====

const CartContext = createContext<CartContextValue | undefined>(undefined);

// ===== Provider =====

interface CartProviderProps {
  children: React.ReactNode;
}

export const CartProvider: React.FC<CartProviderProps> = ({ children }) => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [summary, setSummary] = useState<CartSummary | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch full cart data
   */
  const fetchCart = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await getCart();
      setCart(data);
      setSummary({
        item_count: data.item_count,
        subtotal: data.subtotal,
      });
    } catch (err) {
      console.error('Error fetching cart:', err);
      setError('Failed to load cart');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Fetch lightweight cart summary (for header badge)
   */
  const fetchCartSummary = useCallback(async () => {
    try {
      const data = await getCartSummary();
      setSummary(data);
    } catch (err) {
      console.error('Error fetching cart summary:', err);
    }
  }, []);

  /**
   * Add item to cart
   */
  const addToCart = useCallback(async (data: AddToCartRequest) => {
    try {
      setIsLoading(true);
      setError(null);
      const updatedCart = await addToCartAPI(data);
      setCart(updatedCart);
      setSummary({
        item_count: updatedCart.item_count,
        subtotal: updatedCart.subtotal,
      });
    } catch (err: any) {
      console.error('Error adding to cart:', err);
      const message = err.response?.data?.message || 'Failed to add item to cart';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Update cart item quantity
   */
  const updateCartItem = useCallback(async (productId: string, quantity: number) => {
    try {
      setIsLoading(true);
      setError(null);
      const updatedCart = await updateCartItemAPI(productId, { quantity });
      setCart(updatedCart);
      setSummary({
        item_count: updatedCart.item_count,
        subtotal: updatedCart.subtotal,
      });
    } catch (err: any) {
      console.error('Error updating cart item:', err);
      const message = err.response?.data?.message || 'Failed to update cart';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Remove item from cart
   */
  const removeFromCart = useCallback(async (productId: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const updatedCart = await removeFromCartAPI(productId);
      setCart(updatedCart);
      setSummary({
        item_count: updatedCart.item_count,
        subtotal: updatedCart.subtotal,
      });
    } catch (err: any) {
      console.error('Error removing from cart:', err);
      const message = err.response?.data?.message || 'Failed to remove item';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Clear all items from cart
   */
  const clearCart = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const updatedCart = await clearCartAPI();
      setCart(updatedCart);
      setSummary({
        item_count: 0,
        subtotal: 0,
      });
    } catch (err: any) {
      console.error('Error clearing cart:', err);
      const message = err.response?.data?.message || 'Failed to clear cart';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Refresh cart data (alias for fetchCart)
   */
  const refreshCart = useCallback(async () => {
    await fetchCart();
  }, [fetchCart]);

  // Fetch cart summary on mount
  useEffect(() => {
    fetchCartSummary();
  }, [fetchCartSummary]);

  const value: CartContextValue = {
    cart,
    summary,
    isLoading,
    error,
    fetchCart,
    fetchCartSummary,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    refreshCart,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

// ===== Hook =====

/**
 * Hook to access cart context
 *
 * @throws Error if used outside CartProvider
 */
export const useCart = () => {
  const context = useContext(CartContext);

  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }

  return context;
};
