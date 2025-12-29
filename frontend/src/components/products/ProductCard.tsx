/**
 * ProductCard component for displaying product information.
 *
 * Features:
 * - Product image with hover zoom
 * - Price display with discount badge
 * - Rating display
 * - Stock status
 * - Add to cart button
 * - GSAP hover animations
 * - Responsive design
 * - Accessibility (ARIA labels, keyboard navigation)
 */

import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { Product } from '../../services/api/products';
import Button from '../common/Button';
import { useAnimations } from '../../hooks/useAnimations';

export interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  className?: string;
}

/**
 * ProductCard displays a single product in a card layout.
 *
 * @example
 * ```tsx
 * <ProductCard
 *   product={product}
 *   onAddToCart={handleAddToCart}
 * />
 * ```
 */
export const ProductCard = ({ product, onAddToCart, className = '' }: ProductCardProps) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const { cardHover } = useAnimations();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);

  const handleMouseEnter = () => {
    if (cardRef.current) {
      cardHover(cardRef.current, true);
    }
  };

  const handleMouseLeave = () => {
    if (cardRef.current) {
      cardHover(cardRef.current, false);
    }
  };

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!onAddToCart || !product.is_in_stock) return;

    setIsAddingToCart(true);
    try {
      await onAddToCart(product);
    } finally {
      setIsAddingToCart(false);
    }
  };

  // Format price
  const formattedPrice = `$${product.price.toFixed(2)}`;
  const formattedComparePrice = product.compare_at_price
    ? `$${product.compare_at_price.toFixed(2)}`
    : null;

  // Stock status
  const stockStatus = product.is_low_stock
    ? 'Low Stock'
    : product.is_in_stock
    ? 'In Stock'
    : 'Out of Stock';

  const stockStatusClass = product.is_low_stock
    ? 'text-orange-600'
    : product.is_in_stock
    ? 'text-green-600'
    : 'text-red-600';

  return (
    <div
      ref={cardRef}
      className={`group bg-white rounded-lg shadow-sm overflow-hidden transition-shadow duration-200 hover:shadow-lg ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <Link to={`/products/${product.slug}`} className="block">
        {/* Image Container */}
        <div className="relative aspect-square bg-gray-100 overflow-hidden">
          {/* Product Image */}
          <img
            src={product.images[0]}
            alt={product.name}
            className={`w-full h-full object-cover transition-all duration-500 group-hover:scale-110 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            onLoad={() => setImageLoaded(true)}
            loading="lazy"
          />

          {/* Image Placeholder */}
          {!imageLoaded && (
            <div className="absolute inset-0 flex items-center justify-center">
              <svg
                className="w-12 h-12 text-gray-300 animate-pulse"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
          )}

          {/* Badges */}
          <div className="absolute top-3 left-3 flex flex-col gap-2">
            {/* Discount Badge */}
            {product.discount_percentage && (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-red-600 text-white shadow-sm">
                -{product.discount_percentage}%
              </span>
            )}

            {/* Featured Badge */}
            {product.is_featured && (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-primary-600 text-white shadow-sm">
                Featured
              </span>
            )}
          </div>

          {/* Stock Badge */}
          {!product.is_in_stock && (
            <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span className="px-4 py-2 bg-white text-gray-900 font-semibold rounded-lg">
                Out of Stock
              </span>
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="p-4">
          {/* Product Name */}
          <h3 className="text-base font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">
            {product.name}
          </h3>

          {/* Rating */}
          <div className="flex items-center gap-2 mb-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <svg
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.floor(product.rating)
                      ? 'text-yellow-400 fill-current'
                      : 'text-gray-300'
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                  />
                </svg>
              ))}
            </div>
            <span className="text-sm text-gray-600">({product.review_count})</span>
          </div>

          {/* Price */}
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-xl font-bold text-gray-900">{formattedPrice}</span>
            {formattedComparePrice && (
              <span className="text-sm text-gray-500 line-through">
                {formattedComparePrice}
              </span>
            )}
          </div>

          {/* Stock Status */}
          <p className={`text-sm font-medium mb-3 ${stockStatusClass}`}>{stockStatus}</p>

          {/* Add to Cart Button */}
          <Button
            variant="primary"
            size="sm"
            fullWidth
            onClick={handleAddToCart}
            disabled={!product.is_in_stock || isAddingToCart}
            isLoading={isAddingToCart}
            aria-label={`Add ${product.name} to cart`}
          >
            {product.is_in_stock ? 'Add to Cart' : 'Out of Stock'}
          </Button>
        </div>
      </Link>
    </div>
  );
};

export default ProductCard;
