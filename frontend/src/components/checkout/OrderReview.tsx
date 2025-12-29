/**
 * OrderReview Component
 *
 * Displays order summary for final review before payment.
 * Shows cart items, shipping address, shipping method, and totals.
 */

import React from 'react';
import { Button } from '../common/Button';
import { OrderPreview } from '../../types/address';
import { Cart } from '../../services/api/cart';

interface OrderReviewProps {
  cart: Cart | null;
  orderPreview: OrderPreview | null;
  onEditAddress: () => void;
  onEditShipping: () => void;
  onConfirm: () => void;
  onBack: () => void;
  isLoading?: boolean;
}

export const OrderReview: React.FC<OrderReviewProps> = ({
  cart,
  orderPreview,
  onEditAddress,
  onEditShipping,
  onConfirm,
  onBack,
  isLoading = false,
}) => {
  if (!cart || !orderPreview) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Loading order preview...</p>
      </div>
    );
  }

  const { shipping_address, shipping_method, totals } = orderPreview;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Review Your Order</h2>
        <p className="text-gray-600">Please review your order before proceeding to payment</p>
      </div>

      {/* Order Items */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Order Items</h3>
          <span className="text-sm text-gray-600">
            {cart.item_count} {cart.item_count === 1 ? 'item' : 'items'}
          </span>
        </div>

        <div className="space-y-3">
          {cart.items.map((item) => (
            <div key={item.product_id} className="flex justify-between items-center py-2">
              <div className="flex items-center gap-3">
                {item.product_image && (
                  <img
                    src={item.product_image}
                    alt={item.product_name || 'Product'}
                    className="w-16 h-16 object-cover rounded"
                  />
                )}
                <div>
                  <div className="font-medium text-gray-900">
                    {item.product_name || 'Unknown Product'}
                  </div>
                  <div className="text-sm text-gray-600">
                    Qty: {item.quantity} × ${item.price.toFixed(2)}
                  </div>
                </div>
              </div>
              <div className="font-semibold text-gray-900">
                ${item.item_total.toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Shipping Address */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Shipping Address</h3>
          <button
            onClick={onEditAddress}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Edit
          </button>
        </div>

        {shipping_address && (
          <div className="text-gray-700">
            <p className="font-medium">{shipping_address.full_name}</p>
            <p>{shipping_address.address_line1}</p>
            {shipping_address.address_line2 && <p>{shipping_address.address_line2}</p>}
            <p>
              {shipping_address.city}, {shipping_address.state}{' '}
              {shipping_address.postal_code}
            </p>
            <p>{shipping_address.country}</p>
            {shipping_address.phone && <p className="mt-2">{shipping_address.phone}</p>}
          </div>
        )}
      </div>

      {/* Shipping Method */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Shipping Method</h3>
          <button
            onClick={onEditShipping}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Edit
          </button>
        </div>

        {shipping_method && (
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium text-gray-900">{shipping_method.name}</p>
              <p className="text-sm text-gray-600">{shipping_method.description}</p>
            </div>
            <div className="font-semibold text-gray-900">
              {shipping_method.cost === 0 ? (
                <span className="text-green-600">FREE</span>
              ) : (
                `$${shipping_method.cost.toFixed(2)}`
              )}
            </div>
          </div>
        )}
      </div>

      {/* Order Totals */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>

        <div className="space-y-2">
          <div className="flex justify-between text-gray-700">
            <span>Subtotal</span>
            <span>${totals.subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-gray-700">
            <span>Shipping</span>
            <span>
              {totals.shipping === 0 ? (
                <span className="text-green-600">FREE</span>
              ) : (
                `$${totals.shipping.toFixed(2)}`
              )}
            </span>
          </div>
          <div className="flex justify-between text-gray-700">
            <span>Tax</span>
            <span>${totals.tax.toFixed(2)}</span>
          </div>
          {totals.discount > 0 && (
            <div className="flex justify-between text-green-600">
              <span>Discount</span>
              <span>-${totals.discount.toFixed(2)}</span>
            </div>
          )}
          <div className="border-t border-gray-300 pt-2 mt-2">
            <div className="flex justify-between text-lg font-bold text-gray-900">
              <span>Total</span>
              <span>${totals.total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4 pt-4">
        <Button type="button" variant="outline" onClick={onBack} disabled={isLoading}>
          Back
        </Button>
        <Button
          type="button"
          variant="primary"
          onClick={onConfirm}
          isLoading={isLoading}
          fullWidth
        >
          Proceed to Payment
        </Button>
      </div>
    </div>
  );
};
