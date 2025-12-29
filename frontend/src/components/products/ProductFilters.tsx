/**
 * ProductFilters component for filtering products.
 *
 * Features:
 * - Category filter
 * - Price range filter
 * - Rating filter
 * - Stock status filter
 * - Clear all filters
 * - Mobile-responsive (collapsible on mobile)
 * - Accessibility
 */

import { useState } from 'react';
import { Category } from '../../services/api/categories';
import Button from '../common/Button';
import Input from '../common/Input';

export interface ProductFiltersState {
  category_id?: string;
  min_price?: number;
  max_price?: number;
  min_rating?: number;
  in_stock_only?: boolean;
}

export interface ProductFiltersProps {
  categories: Category[];
  filters: ProductFiltersState;
  onFiltersChange: (filters: ProductFiltersState) => void;
  onClearFilters: () => void;
  className?: string;
}

/**
 * ProductFilters provides UI for filtering products.
 *
 * @example
 * ```tsx
 * <ProductFilters
 *   categories={categories}
 *   filters={filters}
 *   onFiltersChange={setFilters}
 *   onClearFilters={clearFilters}
 * />
 * ```
 */
export const ProductFilters = ({
  categories,
  filters,
  onFiltersChange,
  onClearFilters,
  className = '',
}: ProductFiltersProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [priceMin, setPriceMin] = useState(filters.min_price?.toString() || '');
  const [priceMax, setPriceMax] = useState(filters.max_price?.toString() || '');

  const hasActiveFilters =
    filters.category_id ||
    filters.min_price ||
    filters.max_price ||
    filters.min_rating ||
    filters.in_stock_only;

  const handleCategoryChange = (categoryId: string) => {
    onFiltersChange({
      ...filters,
      category_id: categoryId === filters.category_id ? undefined : categoryId,
    });
  };

  const handlePriceChange = () => {
    const minPrice = priceMin ? parseFloat(priceMin) : undefined;
    const maxPrice = priceMax ? parseFloat(priceMax) : undefined;

    onFiltersChange({
      ...filters,
      min_price: minPrice,
      max_price: maxPrice,
    });
  };

  const handleRatingChange = (rating: number) => {
    onFiltersChange({
      ...filters,
      min_rating: rating === filters.min_rating ? undefined : rating,
    });
  };

  const handleStockFilterChange = () => {
    onFiltersChange({
      ...filters,
      in_stock_only: !filters.in_stock_only,
    });
  };

  const handleClear = () => {
    setPriceMin('');
    setPriceMax('');
    onClearFilters();
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm ${className}`}>
      {/* Mobile Toggle */}
      <button
        className="lg:hidden w-full px-4 py-3 flex items-center justify-between text-left font-semibold text-gray-900 border-b border-gray-200"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls="filter-content"
      >
        <span>Filters {hasActiveFilters && `(${Object.keys(filters).length})`}</span>
        <svg
          className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Filter Content */}
      <div
        id="filter-content"
        className={`${isOpen ? 'block' : 'hidden'} lg:block p-4 space-y-6`}
      >
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={handleClear}>
              Clear All
            </Button>
          )}
        </div>

        {/* Categories */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-3">Categories</h4>
          <div className="space-y-2">
            {categories.map((category) => (
              <label
                key={category._id}
                className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors"
              >
                <input
                  type="checkbox"
                  checked={filters.category_id === category._id}
                  onChange={() => handleCategoryChange(category._id)}
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <span className="ml-3 text-sm text-gray-700">
                  {category.name}
                  {category.product_count !== undefined && (
                    <span className="ml-1 text-gray-500">({category.product_count})</span>
                  )}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Price Range */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-3">Price Range</h4>
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <Input
                type="number"
                placeholder="Min"
                value={priceMin}
                onChange={(e) => setPriceMin(e.target.value)}
                onBlur={handlePriceChange}
                size="sm"
                min={0}
                step={10}
              />
              <Input
                type="number"
                placeholder="Max"
                value={priceMax}
                onChange={(e) => setPriceMax(e.target.value)}
                onBlur={handlePriceChange}
                size="sm"
                min={0}
                step={10}
              />
            </div>
            <Button variant="outline" size="sm" fullWidth onClick={handlePriceChange}>
              Apply
            </Button>
          </div>
        </div>

        {/* Rating Filter */}
        <div>
          <h4 className="font-semibold text-gray-900 mb-3">Minimum Rating</h4>
          <div className="space-y-2">
            {[4, 3, 2, 1].map((rating) => (
              <label
                key={rating}
                className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors"
              >
                <input
                  type="radio"
                  name="rating"
                  checked={filters.min_rating === rating}
                  onChange={() => handleRatingChange(rating)}
                  className="w-4 h-4 text-primary-600 border-gray-300 focus:ring-primary-500"
                />
                <span className="ml-3 flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      className={`w-4 h-4 ${
                        i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
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
                  <span className="ml-2 text-sm text-gray-700">& Up</span>
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Stock Status */}
        <div>
          <label className="flex items-center cursor-pointer hover:bg-gray-50 p-2 rounded transition-colors">
            <input
              type="checkbox"
              checked={filters.in_stock_only || false}
              onChange={handleStockFilterChange}
              className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <span className="ml-3 text-sm font-medium text-gray-700">
              In Stock Only
            </span>
          </label>
        </div>
      </div>
    </div>
  );
};

export default ProductFilters;
