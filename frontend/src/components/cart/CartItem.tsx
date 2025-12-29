/**
 * Cart Item Component
 *
 * Displays a single item in the shopping cart with:
 * - Product image and details
 * - Quantity selector
 * - Remove button
 * - Item total
 */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { CartItem as CartItemType } from '../../services/api/cart';
import { useCart } from '../../contexts/CartContext';

interface CartItemProps {
  item: CartItemType;
}

export const CartItem: React.FC<CartItemProps> = ({ item }) => {
  const { updateCartItem, removeFromCart } = useCart();
  const [isUpdating, setIsUpdating] = useState(false);
  const [isRemoving, setIsRemoving] = useState(false);

  const handleQuantityChange = async (newQuantity: number) => {
    if (newQuantity < 1 || newQuantity > 100) return;
    if (item.product_inventory && newQuantity > item.product_inventory) return;

    try {
      setIsUpdating(true);
      await updateCartItem(item.product_id, newQuantity);
    } catch (error) {
      console.error('Error updating quantity:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleRemove = async () => {
    try {
      setIsRemoving(true);
      await removeFromCart(item.product_id);
    } catch (error) {
      console.error('Error removing item:', error);
      setIsRemoving(false);
    }
  };

  const productSlug = item.product_slug || item.product_id;
  const productName = item.product_name || 'Unknown Product';
  const productImage = item.product_image || 'https://via.placeholder.com/150';
  const inStock = item.product_in_stock ?? true;
  const inventory = item.product_inventory ?? 0;

  return (
    <div
      className={`flex gap-4 py-4 border-b border-gray-200 last:border-0 transition-opacity ${
        isRemoving ? 'opacity-50' : 'opacity-100'
      }`}
    >
      {/* Product Image */}
      <Link
        to={`/products/${productSlug}`}
        className="flex-shrink-0 w-24 h-24 bg-gray-100 rounded-lg overflow-hidden"
      >
        <img
          src={productImage}
          alt={productName}
          className="w-full h-full object-cover"
        />
      </Link>

      {/* Product Details */}
      <div className="flex-1 min-w-0">
        {/* Product Name */}
        <Link
          to={`/products/${productSlug}`}
          className="block text-gray-900 font-medium hover:text-primary-600 transition-colors truncate"
        >
          {productName}
        </Link>

        {/* Price */}
        <p className="mt-1 text-gray-600">
          ${item.price.toFixed(2)}
        </p>

        {/* Stock Status */}
        {!inStock && (
          <p className="mt-1 text-sm text-red-600 font-medium">Out of Stock</p>
        )}
        {inStock && inventory > 0 && inventory < 10 && (
          <p className="mt-1 text-sm text-orange-600">
            Only {inventory} left in stock
          </p>
        )}

        {/* Quantity Selector (Mobile: Below product info) */}
        <div className="flex items-center gap-2 mt-3 md:hidden">
          <button
            onClick={() => handleQuantityChange(item.quantity - 1)}
            disabled={isUpdating || item.quantity <= 1}
            className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            aria-label="Decrease quantity"
          >
            −
          </button>
          <span className="w-12 text-center text-gray-900 font-medium">
            {item.quantity}
          </span>
          <button
            onClick={() => handleQuantityChange(item.quantity + 1)}
            disabled={
              isUpdating ||
              item.quantity >= 100 ||
              (item.product_inventory !== undefined &&
                item.quantity >= item.product_inventory)
            }
            className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            aria-label="Increase quantity"
          >
            +
          </button>

          {/* Remove Button (Mobile) */}
          <button
            onClick={handleRemove}
            disabled={isRemoving}
            className="ml-auto text-sm text-red-600 hover:text-red-700 font-medium disabled:opacity-50 transition-colors"
          >
            Remove
          </button>
        </div>
      </div>

      {/* Quantity Selector (Desktop: Right side) */}
      <div className="hidden md:flex items-center gap-2">
        <button
          onClick={() => handleQuantityChange(item.quantity - 1)}
          disabled={isUpdating || item.quantity <= 1}
          className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Decrease quantity"
        >
          −
        </button>
        <span className="w-12 text-center text-gray-900 font-medium">
          {item.quantity}
        </span>
        <button
          onClick={() => handleQuantityChange(item.quantity + 1)}
          disabled={
            isUpdating ||
            item.quantity >= 100 ||
            (item.product_inventory !== undefined &&
              item.quantity >= item.product_inventory)
          }
          className="w-8 h-8 flex items-center justify-center border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Increase quantity"
        >
          +
        </button>
      </div>

      {/* Item Total (Desktop) */}
      <div className="hidden md:flex flex-col items-end justify-between min-w-[120px]">
        <p className="text-lg font-semibold text-gray-900">
          ${item.item_total.toFixed(2)}
        </p>
        <button
          onClick={handleRemove}
          disabled={isRemoving}
          className="text-sm text-red-600 hover:text-red-700 font-medium disabled:opacity-50 transition-colors"
        >
          Remove
        </button>
      </div>
    </div>
  );
};
