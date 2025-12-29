/**
 * Category API service.
 *
 * Handles all category-related API requests including:
 * - Listing categories
 * - Getting category details
 * - Category product counts
 */

import { apiClient } from './client';

// ===== Types =====

export interface Category {
  _id: string;
  name: string;
  slug: string;
  description: string;
  image_url?: string;
  icon?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  product_count?: number;
}

export interface CategoryListResponse {
  data: Category[];
}

// ===== API Functions =====

/**
 * Get all categories.
 */
export const getCategories = async (
  isActive: boolean = true,
  includeProductCount: boolean = true
): Promise<CategoryListResponse> => {
  const response = await apiClient.get<CategoryListResponse>('/api/categories', {
    params: {
      is_active: isActive,
      include_product_count: includeProductCount,
    },
  });
  return response.data;
};

/**
 * Get a category by ID.
 */
export const getCategoryById = async (categoryId: string): Promise<Category> => {
  const response = await apiClient.get<Category>(`/api/categories/${categoryId}`);
  return response.data;
};

/**
 * Get a category by slug.
 */
export const getCategoryBySlug = async (slug: string): Promise<Category> => {
  const response = await apiClient.get<Category>(`/api/categories/slug/${slug}`);
  return response.data;
};

/**
 * Get product count for a category.
 */
export const getCategoryProductCount = async (categoryId: string): Promise<number> => {
  const response = await apiClient.get<{ category_id: string; product_count: number }>(
    `/api/categories/${categoryId}/product-count`
  );
  return response.data.product_count;
};

// ===== Admin Functions (require authentication) =====

export interface CategoryCreateData {
  _id?: string;
  name: string;
  slug: string;
  description: string;
  image_url?: string;
  icon?: string;
  is_active?: boolean;
}

export interface CategoryUpdateData {
  name?: string;
  slug?: string;
  description?: string;
  image_url?: string;
  icon?: string;
  is_active?: boolean;
}

/**
 * Create a new category (admin only).
 */
export const createCategory = async (data: CategoryCreateData): Promise<Category> => {
  const response = await apiClient.post<Category>('/api/categories', data);
  return response.data;
};

/**
 * Update a category (admin only).
 */
export const updateCategory = async (
  categoryId: string,
  data: CategoryUpdateData
): Promise<Category> => {
  const response = await apiClient.put<Category>(`/api/categories/${categoryId}`, data);
  return response.data;
};

/**
 * Delete a category (admin only).
 */
export const deleteCategory = async (categoryId: string): Promise<void> => {
  await apiClient.delete(`/api/categories/${categoryId}`);
};
