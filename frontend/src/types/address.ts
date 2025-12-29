/**
 * Address types and interfaces
 *
 * Defines types for addresses, shipping methods, and checkout steps.
 */

export enum AddressType {
  SHIPPING = 'shipping',
  BILLING = 'billing',
  BOTH = 'both',
}

export enum ShippingMethodType {
  STANDARD = 'standard',
  EXPRESS = 'express',
  OVERNIGHT = 'overnight',
}

export enum CheckoutStep {
  SHIPPING_INFO = 'shipping_info',
  SHIPPING_METHOD = 'shipping_method',
  REVIEW = 'review',
  PAYMENT = 'payment',
}

export interface Address {
  _id?: string;
  user_id?: string;
  type: AddressType;
  full_name: string;
  address_line1: string;
  address_line2?: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  phone: string;
  is_default: boolean;
}

export interface ShippingMethod {
  method: ShippingMethodType;
  name: string;
  cost: number;
  estimated_days: number;
  description: string;
}

export interface CheckoutTotals {
  subtotal: number;
  shipping: number;
  tax: number;
  discount: number;
  total: number;
}

export interface OrderPreview {
  cart_id: string;
  items_count: number;
  totals: CheckoutTotals;
  shipping_address?: Partial<Address>;
  shipping_method?: ShippingMethod;
  can_proceed: boolean;
  validation_errors: string[];
}

export interface CartValidation {
  valid: boolean;
  errors: string[];
  warnings: string[];
  items_count: number;
  subtotal: number;
}
