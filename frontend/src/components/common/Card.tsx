/**
 * Flexible Card component for content containers.
 *
 * Features:
 * - Header, body, and footer sections
 * - Multiple padding variants
 * - Shadow variants
 * - Hover effects (optional)
 * - Clickable variant with accessible interaction
 * - Border variants
 * - Responsive design
 */

import { HTMLAttributes, ReactNode, forwardRef } from 'react';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** Card header content */
  header?: ReactNode;

  /** Card footer content */
  footer?: ReactNode;

  /** Padding size */
  padding?: 'none' | 'sm' | 'md' | 'lg';

  /** Shadow intensity */
  shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl';

  /** Border variant */
  border?: 'none' | 'light' | 'medium';

  /** Enable hover effect */
  hoverable?: boolean;

  /** Make card clickable */
  clickable?: boolean;

  /** Additional CSS classes */
  className?: string;

  /** Card content */
  children?: ReactNode;
}

/**
 * Card component for organizing content into sections.
 *
 * @example
 * ```tsx
 * <Card
 *   header={<h3>Product Name</h3>}
 *   footer={<Button>Add to Cart</Button>}
 *   hoverable
 * >
 *   <p>Product description goes here...</p>
 * </Card>
 *
 * <Card clickable onClick={handleClick}>
 *   <h4>Clickable Card</h4>
 *   <p>Click anywhere on this card</p>
 * </Card>
 * ```
 */
export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      header,
      footer,
      padding = 'md',
      shadow = 'sm',
      border = 'light',
      hoverable = false,
      clickable = false,
      className = '',
      children,
      onClick,
      ...rest
    },
    ref
  ) => {
    // Base styles
    const baseStyles = 'bg-white rounded-lg transition-all duration-200';

    // Padding styles
    const paddingStyles = {
      none: '',
      sm: 'p-3',
      md: 'p-4 sm:p-6',
      lg: 'p-6 sm:p-8',
    };

    // Shadow styles
    const shadowStyles = {
      none: '',
      sm: 'shadow-sm',
      md: 'shadow-md',
      lg: 'shadow-lg',
      xl: 'shadow-xl',
    };

    // Border styles
    const borderStyles = {
      none: '',
      light: 'border border-gray-200',
      medium: 'border-2 border-gray-300',
    };

    // Interactive styles
    const hoverStyles = hoverable
      ? 'hover:shadow-lg hover:-translate-y-0.5'
      : '';

    const clickableStyles = clickable
      ? 'cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2'
      : '';

    // Combine all styles
    const cardClasses = `${baseStyles} ${paddingStyles[padding]} ${shadowStyles[shadow]} ${borderStyles[border]} ${hoverStyles} ${clickableStyles} ${className}`;

    // Header padding (if no body padding)
    const headerPadding = padding === 'none' ? 'px-4 pt-4 sm:px-6 sm:pt-6' : '';
    const footerPadding = padding === 'none' ? 'px-4 pb-4 sm:px-6 sm:pb-6' : '';

    // Determine if card should be interactive
    const isInteractive = clickable || Boolean(onClick);

    // ARIA role for interactive cards
    const role = isInteractive ? 'button' : undefined;
    const tabIndex = isInteractive ? 0 : undefined;

    // Handle keyboard interaction for clickable cards
    const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
      if (isInteractive && onClick && (e.key === 'Enter' || e.key === ' ')) {
        e.preventDefault();
        onClick(e as any);
      }
    };

    return (
      <div
        ref={ref}
        role={role}
        tabIndex={tabIndex}
        className={cardClasses}
        onClick={isInteractive ? onClick : undefined}
        onKeyDown={handleKeyDown}
        {...rest}
      >
        {/* Header section */}
        {header && (
          <div className={`${headerPadding} ${padding !== 'none' ? 'mb-4' : 'mb-0'}`}>
            {header}
          </div>
        )}

        {/* Body section */}
        {children && <div>{children}</div>}

        {/* Footer section */}
        {footer && (
          <div className={`${footerPadding} ${padding !== 'none' ? 'mt-4 pt-4 border-t border-gray-200' : 'mt-0'}`}>
            {footer}
          </div>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

/**
 * CardHeader - Subcomponent for consistent card headers.
 */
export const CardHeader = forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement>
>(({ className = '', children, ...rest }, ref) => (
  <div
    ref={ref}
    className={`font-semibold text-lg text-gray-900 ${className}`}
    {...rest}
  >
    {children}
  </div>
));

CardHeader.displayName = 'CardHeader';

/**
 * CardTitle - Subcomponent for card titles.
 */
export const CardTitle = forwardRef<
  HTMLHeadingElement,
  HTMLAttributes<HTMLHeadingElement>
>(({ className = '', children, ...rest }, ref) => (
  <h3
    ref={ref}
    className={`font-bold text-xl text-gray-900 ${className}`}
    {...rest}
  >
    {children}
  </h3>
));

CardTitle.displayName = 'CardTitle';

/**
 * CardDescription - Subcomponent for card descriptions.
 */
export const CardDescription = forwardRef<
  HTMLParagraphElement,
  HTMLAttributes<HTMLParagraphElement>
>(({ className = '', children, ...rest }, ref) => (
  <p
    ref={ref}
    className={`text-sm text-gray-600 ${className}`}
    {...rest}
  >
    {children}
  </p>
));

CardDescription.displayName = 'CardDescription';

export default Card;
