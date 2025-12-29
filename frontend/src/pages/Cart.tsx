/**
 * Cart Page
 *
 * Displays the shopping cart with:
 * - List of cart items
 * - Cart summary with totals
 * - Empty cart state
 * - Clear cart option
 */

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { CartItem } from '../components/cart/CartItem';
import { CartSummary } from '../components/cart/CartSummary';
import { Spinner } from '../components/common/Spinner';
import { Modal } from '../components/common/Modal';
import { Button } from '../components/common/Button';

export const Cart: React.FC = () => {
  const { cart, isLoading, error, fetchCart, clearCart } = useCart();
  const [showClearModal, setShowClearModal] = useState(false);
  const [isClearing, setIsClearing] = useState(false);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const handleClearCart = async () => {
    try {
      setIsClearing(true);
      await clearCart();
      setShowClearModal(false);
    } catch (error) {
      console.error('Error clearing cart:', error);
    } finally {
      setIsClearing(false);
    }
  };

  // Loading state
  if (isLoading && !cart) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  // Error state
  if (error && !cart) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={fetchCart}>Try Again</Button>
        </div>
      </div>
    );
  }

  const isEmpty = !cart || cart.items.length === 0;

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>
          {!isEmpty && (
            <p className="mt-2 text-gray-600">
              {cart.item_count} {cart.item_count === 1 ? 'item' : 'items'} in your
              cart
            </p>
          )}
        </div>

        {/* Empty Cart State */}
        {isEmpty && (
          <div className="text-center py-16">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-24 h-24 mx-auto text-gray-400 mb-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
              />
            </svg>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              Your cart is empty
            </h2>
            <p className="text-gray-600 mb-6">
              Add some products to get started!
            </p>
            <Link to="/products">
              <Button variant="primary">Continue Shopping</Button>
            </Link>
          </div>
        )}

        {/* Cart Content */}
        {!isEmpty && cart && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2">
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                {/* Clear Cart Button */}
                <div className="flex justify-end mb-4">
                  <button
                    onClick={() => setShowClearModal(true)}
                    className="text-sm text-red-600 hover:text-red-700 font-medium transition-colors"
                  >
                    Clear Cart
                  </button>
                </div>

                {/* Items List */}
                <div className="divide-y divide-gray-200">
                  {cart.items.map((item) => (
                    <CartItem key={item.product_id} item={item} />
                  ))}
                </div>
              </div>
            </div>

            {/* Cart Summary */}
            <div className="lg:col-span-1">
              <div className="sticky top-8">
                <CartSummary
                  subtotal={cart.subtotal}
                  itemCount={cart.item_count}
                />
              </div>
            </div>
          </div>
        )}

        {/* Clear Cart Confirmation Modal */}
        <Modal
          isOpen={showClearModal}
          onClose={() => setShowClearModal(false)}
          title="Clear Cart"
        >
          <div className="space-y-4">
            <p className="text-gray-700">
              Are you sure you want to remove all items from your cart? This action
              cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <Button
                variant="outline"
                onClick={() => setShowClearModal(false)}
                disabled={isClearing}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleClearCart}
                isLoading={isClearing}
              >
                Clear Cart
              </Button>
            </div>
          </div>
        </Modal>
      </div>
    </div>
  );
};
