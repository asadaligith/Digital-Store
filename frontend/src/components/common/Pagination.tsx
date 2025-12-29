/**
 * Pagination component for navigating through pages of content.
 *
 * Features:
 * - Previous/Next buttons
 * - Page number buttons
 * - Current page indicator
 * - First/Last page shortcuts
 * - Ellipsis for large page counts
 * - Responsive design
 * - Accessibility (ARIA labels, keyboard navigation)
 */

import Button from './Button';

export interface PaginationProps {
  /** Current page number (1-indexed) */
  currentPage: number;

  /** Total number of pages */
  totalPages: number;

  /** Callback when page changes */
  onPageChange: (page: number) => void;

  /** Maximum number of page buttons to show (default: 7) */
  maxButtons?: number;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Pagination component for page navigation.
 *
 * @example
 * ```tsx
 * <Pagination
 *   currentPage={currentPage}
 *   totalPages={totalPages}
 *   onPageChange={setCurrentPage}
 * />
 * ```
 */
export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  maxButtons = 7,
  className = '',
}: PaginationProps) => {
  if (totalPages <= 1) return null;

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const handleFirst = () => {
    onPageChange(1);
  };

  const handleLast = () => {
    onPageChange(totalPages);
  };

  // Generate page numbers to display
  const getPageNumbers = (): (number | string)[] => {
    const pages: (number | string)[] = [];

    if (totalPages <= maxButtons) {
      // Show all pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Show subset with ellipsis
      const halfButtons = Math.floor((maxButtons - 3) / 2);
      const showLeftEllipsis = currentPage > halfButtons + 2;
      const showRightEllipsis = currentPage < totalPages - halfButtons - 1;

      // Always show first page
      pages.push(1);

      if (showLeftEllipsis) {
        pages.push('...');
      }

      // Calculate start and end of middle section
      let start = Math.max(2, currentPage - halfButtons);
      let end = Math.min(totalPages - 1, currentPage + halfButtons);

      // Adjust if at beginning or end
      if (!showLeftEllipsis) {
        end = Math.min(totalPages - 1, maxButtons - 2);
      }
      if (!showRightEllipsis) {
        start = Math.max(2, totalPages - maxButtons + 3);
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (showRightEllipsis) {
        pages.push('...');
      }

      // Always show last page
      if (totalPages > 1) {
        pages.push(totalPages);
      }
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <nav
      className={`flex items-center justify-center gap-2 ${className}`}
      role="navigation"
      aria-label="Pagination"
    >
      {/* First Page Button (hidden on mobile) */}
      <Button
        variant="outline"
        size="sm"
        onClick={handleFirst}
        disabled={currentPage === 1}
        className="hidden sm:inline-flex"
        aria-label="Go to first page"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
          />
        </svg>
      </Button>

      {/* Previous Button */}
      <Button
        variant="outline"
        size="sm"
        onClick={handlePrevious}
        disabled={currentPage === 1}
        aria-label="Go to previous page"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        <span className="sr-only sm:not-sr-only sm:ml-2">Previous</span>
      </Button>

      {/* Page Numbers */}
      <div className="flex items-center gap-1">
        {pageNumbers.map((page, index) => {
          if (page === '...') {
            return (
              <span
                key={`ellipsis-${index}`}
                className="px-2 text-gray-500"
                aria-hidden="true"
              >
                ...
              </span>
            );
          }

          const pageNumber = page as number;
          const isCurrent = pageNumber === currentPage;

          return (
            <button
              key={pageNumber}
              onClick={() => onPageChange(pageNumber)}
              disabled={isCurrent}
              className={`min-w-[40px] h-[40px] px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 ${
                isCurrent
                  ? 'bg-primary-600 text-white cursor-default'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
              }`}
              aria-label={`Go to page ${pageNumber}`}
              aria-current={isCurrent ? 'page' : undefined}
            >
              {pageNumber}
            </button>
          );
        })}
      </div>

      {/* Next Button */}
      <Button
        variant="outline"
        size="sm"
        onClick={handleNext}
        disabled={currentPage === totalPages}
        aria-label="Go to next page"
      >
        <span className="sr-only sm:not-sr-only sm:mr-2">Next</span>
        <svg
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </Button>

      {/* Last Page Button (hidden on mobile) */}
      <Button
        variant="outline"
        size="sm"
        onClick={handleLast}
        disabled={currentPage === totalPages}
        className="hidden sm:inline-flex"
        aria-label="Go to last page"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M13 5l7 7-7 7M5 5l7 7-7 7"
          />
        </svg>
      </Button>
    </nav>
  );
};

export default Pagination;
