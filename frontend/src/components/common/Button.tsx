/**
 * Accessible Button component with multiple variants and states.
 *
 * Features:
 * - Multiple variants: primary, secondary, outline, ghost, danger
 * - Multiple sizes: sm, md, lg
 * - Loading state with spinner
 * - Icon support (leading/trailing)
 * - Full keyboard navigation
 * - Touch targets ≥44px for mobile accessibility
 * - ARIA labels and states
 */

import { ButtonHTMLAttributes, ReactNode, forwardRef } from 'react';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual variant of the button */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';

  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';

  /** Loading state - shows spinner and disables interaction */
  isLoading?: boolean;

  /** Full width button */
  fullWidth?: boolean;

  /** Icon to display before the text */
  leftIcon?: ReactNode;

  /** Icon to display after the text */
  rightIcon?: ReactNode;

  /** Additional CSS classes */
  className?: string;

  /** Button content */
  children?: ReactNode;
}

/**
 * Button component with accessibility and mobile-first design.
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   Click me
 * </Button>
 *
 * <Button variant="secondary" isLoading leftIcon={<IconUser />}>
 *   Save Profile
 * </Button>
 * ```
 */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      fullWidth = false,
      leftIcon,
      rightIcon,
      className = '',
      children,
      disabled,
      type = 'button',
      ...rest
    },
    ref
  ) => {
    // Base styles - always applied
    const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed';

    // Variant styles
    const variantStyles = {
      primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 focus-visible:ring-primary-500',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 active:bg-gray-400 focus-visible:ring-gray-500',
      outline: 'border-2 border-primary-600 text-primary-600 bg-transparent hover:bg-primary-50 active:bg-primary-100 focus-visible:ring-primary-500',
      ghost: 'text-gray-700 bg-transparent hover:bg-gray-100 active:bg-gray-200 focus-visible:ring-gray-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 focus-visible:ring-red-500',
    };

    // Size styles (ensuring touch targets ≥44px for mobile)
    const sizeStyles = {
      sm: 'px-3 py-2 text-sm min-h-[44px]', // 44px minimum for touch
      md: 'px-4 py-2.5 text-base min-h-[48px]', // 48px comfortable default
      lg: 'px-6 py-3 text-lg min-h-[52px]', // 52px for prominent actions
    };

    // Width styles
    const widthStyles = fullWidth ? 'w-full' : '';

    // Combine all styles
    const buttonClasses = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${widthStyles} ${className}`;

    // Icon wrapper styles
    const iconWrapperStyles = 'inline-flex items-center justify-center';

    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || isLoading}
        className={buttonClasses}
        aria-busy={isLoading}
        aria-disabled={disabled || isLoading}
        {...rest}
      >
        {/* Loading spinner */}
        {isLoading && (
          <svg
            className={`animate-spin -ml-1 mr-2 h-4 w-4 ${iconWrapperStyles}`}
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}

        {/* Left icon */}
        {!isLoading && leftIcon && (
          <span className={`mr-2 ${iconWrapperStyles}`} aria-hidden="true">
            {leftIcon}
          </span>
        )}

        {/* Button text */}
        {children && <span>{children}</span>}

        {/* Right icon */}
        {!isLoading && rightIcon && (
          <span className={`ml-2 ${iconWrapperStyles}`} aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
