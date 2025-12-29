/**
 * Validation utilities for forms
 *
 * Provides validation functions for common input types.
 */

/**
 * Validate email address
 */
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate phone number
 * Accepts various formats: +1-555-123-4567, (555) 123-4567, 555.123.4567, etc.
 */
export const validatePhone = (phone: string): boolean => {
  // Remove common separators
  const cleaned = phone.replace(/[\s\-\(\)\.]/g, '');

  // Check if it contains only digits and optional + prefix
  const phoneRegex = /^\+?\d{10,15}$/;
  return phoneRegex.test(cleaned);
};

/**
 * Validate US postal code (ZIP code)
 * Accepts: 12345 or 12345-6789
 */
export const validatePostalCode = (postalCode: string, country: string = 'US'): boolean => {
  if (country === 'US') {
    const usZipRegex = /^\d{5}(-\d{4})?$/;
    return usZipRegex.test(postalCode);
  }

  // For other countries, allow alphanumeric with spaces/hyphens
  const generalRegex = /^[A-Z0-9\s\-]{3,10}$/i;
  return generalRegex.test(postalCode);
};

/**
 * Validate required field
 */
export const validateRequired = (value: string | undefined | null): boolean => {
  return value !== undefined && value !== null && value.trim().length > 0;
};

/**
 * Validate minimum length
 */
export const validateMinLength = (value: string, minLength: number): boolean => {
  return value.length >= minLength;
};

/**
 * Validate maximum length
 */
export const validateMaxLength = (value: string, maxLength: number): boolean => {
  return value.length <= maxLength;
};

/**
 * Validate US state code (2 letters)
 */
export const validateStateCode = (state: string): boolean => {
  const stateRegex = /^[A-Z]{2}$/;
  return stateRegex.test(state.toUpperCase());
};

/**
 * Validate country code (2 letters, ISO 3166-1 alpha-2)
 */
export const validateCountryCode = (country: string): boolean => {
  const countryRegex = /^[A-Z]{2}$/;
  return countryRegex.test(country.toUpperCase());
};

/**
 * Get error message for validation failure
 */
export const getValidationError = (
  field: string,
  validationType: string
): string => {
  const errorMessages: Record<string, Record<string, string>> = {
    email: {
      invalid: 'Please enter a valid email address',
    },
    phone: {
      invalid: 'Please enter a valid phone number',
    },
    postal_code: {
      invalid: 'Please enter a valid postal code',
    },
    required: {
      invalid: `${field} is required`,
    },
    state: {
      invalid: 'Please enter a valid 2-letter state code',
    },
    country: {
      invalid: 'Please enter a valid 2-letter country code',
    },
  };

  return errorMessages[field]?.[validationType] || `Invalid ${field}`;
};
