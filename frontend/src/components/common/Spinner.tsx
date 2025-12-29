/**
 * Accessible Spinner component for loading states.
 *
 * Features:
 * - Multiple sizes (xs, sm, md, lg, xl)
 * - Multiple color variants
 * - Text label support
 * - ARIA live region for screen readers
 * - Center overlay variant (full screen loading)
 * - Customizable speed
 */

import { HTMLAttributes, forwardRef } from 'react';

export interface SpinnerProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
  /** Spinner size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';

  /** Spinner color variant */
  variant?: 'primary' | 'secondary' | 'white' | 'gray';

  /** Loading text (shown to screen readers and optionally displayed) */
  label?: string;

  /** Whether to show the label text */
  showLabel?: boolean;

  /** Whether to center the spinner with a full-screen overlay */
  overlay?: boolean;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Spinner component for indicating loading states.
 *
 * @example
 * ```tsx
 * <Spinner size="md" label="Loading products..." />
 *
 * <Spinner size="sm" variant="white" />
 *
 * <Spinner overlay label="Processing payment..." showLabel />
 * ```
 */
export const Spinner = forwardRef<HTMLDivElement, SpinnerProps>(
  (
    {
      size = 'md',
      variant = 'primary',
      label = 'Loading...',
      showLabel = false,
      overlay = false,
      className = '',
      ...rest
    },
    ref
  ) => {
    // Size styles
    const sizeStyles = {
      xs: 'w-3 h-3 border-2',
      sm: 'w-4 h-4 border-2',
      md: 'w-6 h-6 border-2',
      lg: 'w-8 h-8 border-3',
      xl: 'w-12 h-12 border-4',
    };

    // Color variant styles
    const variantStyles = {
      primary: 'border-primary-600 border-t-transparent',
      secondary: 'border-gray-600 border-t-transparent',
      white: 'border-white border-t-transparent',
      gray: 'border-gray-400 border-t-transparent',
    };

    // Base spinner styles
    const spinnerClasses = `inline-block rounded-full animate-spin ${sizeStyles[size]} ${variantStyles[variant]}`;

    // Container wrapper
    const SpinnerContent = (
      <div
        ref={ref}
        className={`flex items-center justify-center ${className}`}
        role="status"
        aria-live="polite"
        aria-busy="true"
        {...rest}
      >
        {/* Spinner circle */}
        <div className={spinnerClasses} aria-hidden="true" />

        {/* Label */}
        {showLabel && label && (
          <span className="ml-3 text-sm font-medium text-gray-700">
            {label}
          </span>
        )}

        {/* Screen reader only text */}
        {!showLabel && label && (
          <span className="sr-only">{label}</span>
        )}
      </div>
    );

    // Render with overlay if requested
    if (overlay) {
      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
          <div className="bg-white rounded-lg shadow-xl p-6">
            {SpinnerContent}
          </div>
        </div>
      );
    }

    return SpinnerContent;
  }
);

Spinner.displayName = 'Spinner';

/**
 * Inline spinner for buttons and small spaces.
 */
export const InlineSpinner = forwardRef<
  HTMLDivElement,
  Omit<SpinnerProps, 'showLabel' | 'overlay'>
>(({ size = 'sm', className = '', ...rest }, ref) => (
  <Spinner
    ref={ref}
    size={size}
    showLabel={false}
    overlay={false}
    className={`inline-flex ${className}`}
    {...rest}
  />
));

InlineSpinner.displayName = 'InlineSpinner';

/**
 * Full page loading spinner.
 */
export const PageSpinner = forwardRef<
  HTMLDivElement,
  Omit<SpinnerProps, 'overlay'>
>(({ size = 'lg', showLabel = true, className = '', ...rest }, ref) => (
  <Spinner
    ref={ref}
    size={size}
    showLabel={showLabel}
    overlay={true}
    className={className}
    {...rest}
  />
));

PageSpinner.displayName = 'PageSpinner';

export default Spinner;
