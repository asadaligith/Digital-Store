/**
 * Product API service.
 *
 * Handles all product-related API requests including:
 * - Listing products with filtering and pagination
 * - Getting product details
 * - Featured products
 * - Products by category
 */

import { apiClient } from './client';
import type { ApiResponse, ApiListResponse, PaginationMeta } from '../../types/api';

// ===== Types =====

export interface Product {
  _id: string;
  name: string;
  slug: string;
  description: string;
  category_id: string;
  price: number;
  compare_at_price?: number;
  sku: string;
  inventory_quantity: number;
  images: string[];
  is_featured: boolean;
  is_active: boolean;
  rating: number;
  review_count: number;
  created_at: string;
  updated_at: string;
  discount_percentage?: number;
  is_in_stock: boolean;
  is_low_stock: boolean;
}

export interface ProductListParams {
  page?: number;
  limit?: number;
  search?: string;
  category_id?: string;
  min_price?: number;
  max_price?: number;
  min_rating?: number;
  is_featured?: boolean;
  in_stock_only?: boolean;
  sort_by?: 'created_at' | 'price' | 'name' | 'rating' | 'review_count';
  sort_order?: 'asc' | 'desc';
}

export interface ProductListResponse {
  data: Product[];
  meta: PaginationMeta;
}

// ===== API Functions =====

/**
 * Get a list of products with filtering and pagination.
 */
export const getProducts = async (params?: ProductListParams): Promise<ProductListResponse> => {
  const response = await apiClient.get<ProductListResponse>('/api/products', { params });
  return response.data;
};

/**
 * Get a product by ID.
 */
export const getProductById = async (productId: string): Promise<Product> => {
  const response = await apiClient.get<Product>(`/api/products/${productId}`);
  return response.data;
};

/**
 * Get a product by slug.
 */
export const getProductBySlug = async (slug: string): Promise<Product> => {
  const response = await apiClient.get<Product>(`/api/products/slug/${slug}`);
  return response.data;
};

/**
 * Get featured products for homepage.
 */
export const getFeaturedProducts = async (limit: number = 8): Promise<ProductListResponse> => {
  const response = await apiClient.get<ProductListResponse>('/api/products/featured', {
    params: { limit },
  });
  return response.data;
};

/**
 * Get products by category.
 */
export const getProductsByCategory = async (
  categoryId: string,
  page: number = 1,
  limit: number = 20
): Promise<ProductListResponse> => {
  const response = await apiClient.get<ProductListResponse>(
    `/api/products/category/${categoryId}`,
    {
      params: { page, limit },
    }
  );
  return response.data;
};

// ===== Admin Functions (require authentication) =====

export interface ProductCreateData {
  name: string;
  slug: string;
  description: string;
  category_id: string;
  price: number;
  compare_at_price?: number;
  sku: string;
  inventory_quantity: number;
  images: string[];
  is_featured?: boolean;
  is_active?: boolean;
}

export interface ProductUpdateData {
  name?: string;
  slug?: string;
  description?: string;
  category_id?: string;
  price?: number;
  compare_at_price?: number;
  sku?: string;
  inventory_quantity?: number;
  images?: string[];
  is_featured?: boolean;
  is_active?: boolean;
}

/**
 * Create a new product (admin only).
 */
export const createProduct = async (data: ProductCreateData): Promise<Product> => {
  const response = await apiClient.post<Product>('/api/products', data);
  return response.data;
};

/**
 * Update a product (admin only).
 */
export const updateProduct = async (
  productId: string,
  data: ProductUpdateData
): Promise<Product> => {
  const response = await apiClient.put<Product>(`/api/products/${productId}`, data);
  return response.data;
};

/**
 * Delete a product (admin only).
 */
export const deleteProduct = async (productId: string): Promise<void> => {
  await apiClient.delete(`/api/products/${productId}`);
};

/**
 * Update product inventory (admin only).
 */
export const updateProductInventory = async (
  productId: string,
  quantityChange: number
): Promise<Product> => {
  const response = await apiClient.patch<Product>(
    `/api/products/${productId}/inventory`,
    null,
    {
      params: { quantity_change: quantityChange },
    }
  );
  return response.data;
};
