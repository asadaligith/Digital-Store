/**
 * ProductSort component for sorting products.
 *
 * Features:
 * - Multiple sort options (price, name, rating, date)
 * - Dropdown select interface
 * - Responsive design
 * - Accessibility
 */

export interface ProductSortOption {
  label: string;
  value: string;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
}

export interface ProductSortProps {
  value: string;
  onChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  className?: string;
}

/**
 * Available sort options.
 */
export const SORT_OPTIONS: ProductSortOption[] = [
  {
    label: 'Newest',
    value: 'created_at:desc',
    sortBy: 'created_at',
    sortOrder: 'desc',
  },
  {
    label: 'Price: Low to High',
    value: 'price:asc',
    sortBy: 'price',
    sortOrder: 'asc',
  },
  {
    label: 'Price: High to Low',
    value: 'price:desc',
    sortBy: 'price',
    sortOrder: 'desc',
  },
  {
    label: 'Name: A-Z',
    value: 'name:asc',
    sortBy: 'name',
    sortOrder: 'asc',
  },
  {
    label: 'Name: Z-A',
    value: 'name:desc',
    sortBy: 'name',
    sortOrder: 'desc',
  },
  {
    label: 'Highest Rated',
    value: 'rating:desc',
    sortBy: 'rating',
    sortOrder: 'desc',
  },
  {
    label: 'Most Popular',
    value: 'review_count:desc',
    sortBy: 'review_count',
    sortOrder: 'desc',
  },
];

/**
 * ProductSort provides a dropdown for sorting products.
 *
 * @example
 * ```tsx
 * <ProductSort
 *   value="price:asc"
 *   onChange={(sortBy, sortOrder) => setSorting({ sortBy, sortOrder })}
 * />
 * ```
 */
export const ProductSort = ({ value, onChange, className = '' }: ProductSortProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOption = SORT_OPTIONS.find((opt) => opt.value === e.target.value);
    if (selectedOption) {
      onChange(selectedOption.sortBy, selectedOption.sortOrder);
    }
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <label
        htmlFor="product-sort"
        className="text-sm font-medium text-gray-700 whitespace-nowrap"
      >
        Sort by:
      </label>
      <select
        id="product-sort"
        value={value}
        onChange={handleChange}
        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
        aria-label="Sort products"
      >
        {SORT_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ProductSort;
