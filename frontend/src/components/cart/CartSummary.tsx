/**
 * Cart Summary Component
 *
 * Displays cart totals and checkout button.
 * Shows subtotal, tax, shipping, and total.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../common/Button';

interface CartSummaryProps {
  subtotal: number;
  itemCount: number;
  onCheckout?: () => void;
  className?: string;
}

export const CartSummary: React.FC<CartSummaryProps> = ({
  subtotal,
  itemCount,
  onCheckout,
  className = '',
}) => {
  const navigate = useNavigate();

  // Calculate estimated tax (8% for demo)
  const taxRate = 0.08;
  const tax = subtotal * taxRate;

  // Free shipping over $50, otherwise $5.99
  const shipping = subtotal >= 50 ? 0 : 5.99;

  // Calculate total
  const total = subtotal + tax + shipping;

  const handleCheckout = () => {
    if (onCheckout) {
      onCheckout();
    } else {
      // Navigate to checkout page (to be implemented in Phase 5)
      navigate('/checkout');
    }
  };

  return (
    <div className={`bg-gray-50 rounded-lg p-6 ${className}`}>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h2>

      {/* Subtotal */}
      <div className="flex justify-between text-gray-700 mb-2">
        <span>Subtotal ({itemCount} {itemCount === 1 ? 'item' : 'items'})</span>
        <span>${subtotal.toFixed(2)}</span>
      </div>

      {/* Shipping */}
      <div className="flex justify-between text-gray-700 mb-2">
        <span>Shipping</span>
        <span className={shipping === 0 ? 'text-green-600 font-medium' : ''}>
          {shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`}
        </span>
      </div>

      {/* Free Shipping Notice */}
      {subtotal > 0 && subtotal < 50 && (
        <p className="text-sm text-gray-600 mb-2">
          Add ${(50 - subtotal).toFixed(2)} more for free shipping
        </p>
      )}

      {/* Estimated Tax */}
      <div className="flex justify-between text-gray-700 mb-4">
        <span>Estimated Tax</span>
        <span>${tax.toFixed(2)}</span>
      </div>

      {/* Divider */}
      <div className="border-t border-gray-300 my-4"></div>

      {/* Total */}
      <div className="flex justify-between text-gray-900 font-semibold text-lg mb-6">
        <span>Total</span>
        <span>${total.toFixed(2)}</span>
      </div>

      {/* Checkout Button */}
      <Button
        variant="primary"
        fullWidth
        onClick={handleCheckout}
        disabled={itemCount === 0}
      >
        Proceed to Checkout
      </Button>

      {/* Continue Shopping Link */}
      <button
        onClick={() => navigate('/products')}
        className="w-full mt-3 text-center text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors"
      >
        Continue Shopping
      </button>

      {/* Security Badge */}
      <div className="mt-6 pt-6 border-t border-gray-300">
        <div className="flex items-center justify-center gap-2 text-sm text-gray-600">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-5 h-5 text-green-600"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
            />
          </svg>
          <span>Secure Checkout</span>
        </div>
      </div>
    </div>
  );
};
