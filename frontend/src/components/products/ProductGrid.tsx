/**
 * ProductGrid component for displaying products in a responsive grid.
 *
 * Features:
 * - Responsive grid layout (1-4 columns based on screen size)
 * - GSAP stagger animations
 * - Loading skeleton
 * - Empty state
 * - Accessibility
 */

import { useEffect, useRef } from 'react';
import { Product } from '../../services/api/products';
import ProductCard from './ProductCard';
import Spinner from '../common/Spinner';
import { useAnimations } from '../../hooks/useAnimations';

export interface ProductGridProps {
  products: Product[];
  isLoading?: boolean;
  onAddToCart?: (product: Product) => void;
  className?: string;
}

/**
 * ProductGrid displays products in a responsive grid layout.
 *
 * @example
 * ```tsx
 * <ProductGrid
 *   products={products}
 *   isLoading={isLoading}
 *   onAddToCart={handleAddToCart}
 * />
 * ```
 */
export const ProductGrid = ({
  products,
  isLoading = false,
  onAddToCart,
  className = '',
}: ProductGridProps) => {
  const gridRef = useRef<HTMLDivElement>(null);
  const { staggerIn } = useAnimations();

  // Animate products on mount or when products change
  useEffect(() => {
    if (!isLoading && products.length > 0 && gridRef.current) {
      const cards = gridRef.current.querySelectorAll('.product-card');
      staggerIn(cards, {
        duration: 0.5,
        stagger: 0.08,
        from: 'start',
      });
    }
  }, [products, isLoading, staggerIn]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-16">
        <Spinner size="lg" label="Loading products..." showLabel />
      </div>
    );
  }

  // Empty state
  if (products.length === 0) {
    return (
      <div className="text-center py-16">
        <svg
          className="mx-auto h-16 w-16 text-gray-400 mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
          />
        </svg>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No products found</h3>
        <p className="text-gray-600">Try adjusting your filters or search query.</p>
      </div>
    );
  }

  return (
    <div
      ref={gridRef}
      className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 ${className}`}
      role="list"
      aria-label="Products"
    >
      {products.map((product) => (
        <div key={product._id} className="product-card" role="listitem">
          <ProductCard product={product} onAddToCart={onAddToCart} />
        </div>
      ))}
    </div>
  );
};

/**
 * ProductGridSkeleton - Loading skeleton for product grid.
 */
export const ProductGridSkeleton = ({ count = 8 }: { count?: number }) => {
  return (
    <div
      className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      aria-busy="true"
      aria-label="Loading products"
    >
      {[...Array(count)].map((_, i) => (
        <div key={i} className="bg-white rounded-lg shadow-sm overflow-hidden animate-pulse">
          {/* Image skeleton */}
          <div className="aspect-square bg-gray-200" />

          {/* Content skeleton */}
          <div className="p-4 space-y-3">
            {/* Title */}
            <div className="h-4 bg-gray-200 rounded w-3/4" />
            <div className="h-4 bg-gray-200 rounded w-1/2" />

            {/* Rating */}
            <div className="h-4 bg-gray-200 rounded w-1/3" />

            {/* Price */}
            <div className="h-6 bg-gray-200 rounded w-1/4" />

            {/* Button */}
            <div className="h-10 bg-gray-200 rounded" />
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;
