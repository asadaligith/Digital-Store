/**
 * Global API types and interfaces.
 */

export interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  pages: number;
}

export interface ApiError {
  code: string;
  message: string;
  status: number;
  details?: Record<string, any>;
}

export interface ApiListResponse<T> {
  data: T[];
  meta: PaginationMeta;
}
