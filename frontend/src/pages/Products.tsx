/**
 * Products page - Browse and filter products.
 *
 * Features:
 * - Product grid with filtering and sorting
 * - Category filter sidebar
 * - Price and rating filters
 * - Search functionality
 * - Pagination
 * - Responsive layout
 * - Loading and error states
 */

import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getProducts, Product } from '../services/api/products';
import { getCategories, Category } from '../services/api/categories';
import { useCart } from '../contexts/CartContext';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import ProductGrid from '../components/products/ProductGrid';
import ProductFilters, { ProductFiltersState } from '../components/products/ProductFilters';
import ProductSort, { SORT_OPTIONS } from '../components/products/ProductSort';
import Pagination from '../components/common/Pagination';
import Spinner from '../components/common/Spinner';

export const Products = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const { addToCart } = useCart();

  // State
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalProducts, setTotalProducts] = useState(0);

  // Filters
  const [filters, setFilters] = useState<ProductFiltersState>({});

  // Sorting
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Search
  const [searchQuery, setSearchQuery] = useState('');

  // Initialize from URL params
  useEffect(() => {
    const page = parseInt(searchParams.get('page') || '1', 10);
    const search = searchParams.get('search') || '';
    const categoryId = searchParams.get('category') || undefined;
    const minPrice = searchParams.get('min_price');
    const maxPrice = searchParams.get('max_price');
    const minRating = searchParams.get('min_rating');
    const inStock = searchParams.get('in_stock_only');
    const sort = searchParams.get('sort') || 'created_at:desc';

    setCurrentPage(page);
    setSearchQuery(search);
    setFilters({
      category_id: categoryId,
      min_price: minPrice ? parseFloat(minPrice) : undefined,
      max_price: maxPrice ? parseFloat(maxPrice) : undefined,
      min_rating: minRating ? parseFloat(minRating) : undefined,
      in_stock_only: inStock === 'true',
    });

    const sortOption = SORT_OPTIONS.find((opt) => opt.value === sort);
    if (sortOption) {
      setSortBy(sortOption.sortBy);
      setSortOrder(sortOption.sortOrder);
    }
  }, [searchParams]);

  // Fetch categories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await getCategories(true, true);
        setCategories(response.data);
      } catch (err) {
        console.error('Failed to fetch categories:', err);
      }
    };

    fetchCategories();
  }, []);

  // Fetch products
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await getProducts({
          page: currentPage,
          limit: 20,
          search: searchQuery || undefined,
          category_id: filters.category_id,
          min_price: filters.min_price,
          max_price: filters.max_price,
          min_rating: filters.min_rating,
          in_stock_only: filters.in_stock_only,
          sort_by: sortBy as any,
          sort_order: sortOrder,
        });

        setProducts(response.data);
        setTotalPages(response.meta.pages);
        setTotalProducts(response.meta.total);
      } catch (err: any) {
        setError(err.message || 'Failed to load products');
        console.error('Failed to fetch products:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [currentPage, searchQuery, filters, sortBy, sortOrder]);

  // Update URL params
  const updateUrlParams = (updates: Record<string, string | undefined>) => {
    const newParams = new URLSearchParams(searchParams);

    Object.entries(updates).forEach(([key, value]) => {
      if (value) {
        newParams.set(key, value);
      } else {
        newParams.delete(key);
      }
    });

    setSearchParams(newParams);
  };

  // Handlers
  const handleFiltersChange = (newFilters: ProductFiltersState) => {
    setFilters(newFilters);
    setCurrentPage(1);
    updateUrlParams({
      page: '1',
      category: newFilters.category_id,
      min_price: newFilters.min_price?.toString(),
      max_price: newFilters.max_price?.toString(),
      min_rating: newFilters.min_rating?.toString(),
      in_stock_only: newFilters.in_stock_only ? 'true' : undefined,
    });
  };

  const handleClearFilters = () => {
    setFilters({});
    setCurrentPage(1);
    updateUrlParams({
      page: '1',
      category: undefined,
      min_price: undefined,
      max_price: undefined,
      min_rating: undefined,
      in_stock_only: undefined,
    });
  };

  const handleSortChange = (newSortBy: string, newSortOrder: 'asc' | 'desc') => {
    setSortBy(newSortBy);
    setSortOrder(newSortOrder);
    setCurrentPage(1);
    updateUrlParams({
      page: '1',
      sort: `${newSortBy}:${newSortOrder}`,
    });
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    updateUrlParams({ page: page.toString() });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAddToCart = async (product: Product) => {
    try {
      await addToCart({
        product_id: product._id,
        quantity: 1,
      });
      // Success feedback could be added here (toast notification, etc.)
    } catch (error: any) {
      console.error('Failed to add to cart:', error);
      alert(error.message || 'Failed to add item to cart');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />

      <main className="flex-1">
        <div className="container-custom py-8">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Products</h1>
            <p className="text-gray-600">
              {totalProducts} {totalProducts === 1 ? 'product' : 'products'} found
            </p>
          </div>

          {/* Layout: Sidebar + Content */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Filters Sidebar */}
            <aside className="lg:col-span-1">
              <ProductFilters
                categories={categories}
                filters={filters}
                onFiltersChange={handleFiltersChange}
                onClearFilters={handleClearFilters}
              />
            </aside>

            {/* Main Content */}
            <div className="lg:col-span-3">
              {/* Toolbar: Sort + Results Count */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <p className="text-sm text-gray-600">
                  Showing {products.length > 0 ? (currentPage - 1) * 20 + 1 : 0} -{' '}
                  {Math.min(currentPage * 20, totalProducts)} of {totalProducts} products
                </p>
                <ProductSort
                  value={`${sortBy}:${sortOrder}`}
                  onChange={handleSortChange}
                />
              </div>

              {/* Error State */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              {/* Product Grid */}
              <ProductGrid
                products={products}
                isLoading={isLoading}
                onAddToCart={handleAddToCart}
              />

              {/* Pagination */}
              {!isLoading && totalPages > 1 && (
                <div className="mt-8">
                  <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={handlePageChange}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Products;
