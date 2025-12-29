/**
 * Accessible Input component with validation states and error handling.
 *
 * Features:
 * - Multiple input types (text, email, password, number, tel, url, search)
 * - Validation states (default, error, success)
 * - Error and helper text support
 * - Label with required indicator
 * - Icon support (leading/trailing)
 * - Full keyboard navigation
 * - Touch-friendly sizing (≥44px)
 * - ARIA labels and error associations
 */

import { InputHTMLAttributes, ReactNode, forwardRef, useId } from 'react';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Input label text */
  label?: string;

  /** Helper text displayed below the input */
  helperText?: string;

  /** Error message - when provided, input displays error state */
  error?: string;

  /** Success state - shows success styling */
  isSuccess?: boolean;

  /** Icon to display before the input */
  leftIcon?: ReactNode;

  /** Icon to display after the input */
  rightIcon?: ReactNode;

  /** Input size */
  size?: 'sm' | 'md' | 'lg';

  /** Additional CSS classes for the input element */
  inputClassName?: string;

  /** Additional CSS classes for the wrapper */
  className?: string;
}

/**
 * Input component with accessibility and validation support.
 *
 * @example
 * ```tsx
 * <Input
 *   label="Email"
 *   type="email"
 *   placeholder="you@example.com"
 *   required
 *   error={errors.email}
 * />
 *
 * <Input
 *   label="Search"
 *   type="search"
 *   leftIcon={<IconSearch />}
 *   helperText="Search for products..."
 * />
 * ```
 */
export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      isSuccess = false,
      leftIcon,
      rightIcon,
      size = 'md',
      inputClassName = '',
      className = '',
      id: providedId,
      required = false,
      disabled = false,
      type = 'text',
      ...rest
    },
    ref
  ) => {
    // Generate unique IDs for accessibility
    const generatedId = useId();
    const id = providedId || generatedId;
    const errorId = `${id}-error`;
    const helperId = `${id}-helper`;

    // Determine validation state
    const hasError = Boolean(error);
    const showSuccess = isSuccess && !hasError;

    // Base input styles
    const baseInputStyles = 'w-full rounded-lg border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-60 disabled:cursor-not-allowed disabled:bg-gray-100';

    // Size styles (ensuring touch targets ≥44px)
    const sizeStyles = {
      sm: 'px-3 py-2 text-sm min-h-[44px]',
      md: 'px-4 py-2.5 text-base min-h-[48px]',
      lg: 'px-5 py-3 text-lg min-h-[52px]',
    };

    // Validation state styles
    const stateStyles = hasError
      ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
      : showSuccess
      ? 'border-green-500 focus:border-green-500 focus:ring-green-500'
      : 'border-gray-300 focus:border-primary-500 focus:ring-primary-500';

    // Icon padding adjustments
    const leftIconPadding = leftIcon ? 'pl-10' : '';
    const rightIconPadding = rightIcon ? 'pr-10' : '';

    // Combine input classes
    const inputClasses = `${baseInputStyles} ${sizeStyles[size]} ${stateStyles} ${leftIconPadding} ${rightIconPadding} ${inputClassName}`;

    return (
      <div className={`w-full ${className}`}>
        {/* Label */}
        {label && (
          <label
            htmlFor={id}
            className="block text-sm font-semibold text-gray-700 mb-1.5"
          >
            {label}
            {required && (
              <span className="text-red-500 ml-1" aria-label="required">
                *
              </span>
            )}
          </label>
        )}

        {/* Input wrapper for icon positioning */}
        <div className="relative">
          {/* Left icon */}
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
              {leftIcon}
            </div>
          )}

          {/* Input field */}
          <input
            ref={ref}
            id={id}
            type={type}
            disabled={disabled}
            required={required}
            className={inputClasses}
            aria-invalid={hasError}
            aria-describedby={
              hasError
                ? errorId
                : helperText
                ? helperId
                : undefined
            }
            {...rest}
          />

          {/* Right icon */}
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
              {rightIcon}
            </div>
          )}

          {/* Success indicator */}
          {showSuccess && !rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500 pointer-events-none">
              <svg
                className="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          )}

          {/* Error indicator */}
          {hasError && !rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-red-500 pointer-events-none">
              <svg
                className="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 20 20"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          )}
        </div>

        {/* Error message */}
        {hasError && (
          <p
            id={errorId}
            className="mt-1.5 text-sm text-red-600"
            role="alert"
          >
            {error}
          </p>
        )}

        {/* Helper text */}
        {!hasError && helperText && (
          <p
            id={helperId}
            className="mt-1.5 text-sm text-gray-500"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
