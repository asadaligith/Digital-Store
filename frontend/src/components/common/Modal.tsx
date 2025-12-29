/**
 * Accessible Modal component with focus management and animations.
 *
 * Features:
 * - Portal rendering (renders outside DOM hierarchy)
 * - Focus trap (keeps focus inside modal)
 * - Escape key to close
 * - Click outside to close (optional)
 * - Overlay backdrop with animation
 * - Body scroll lock when open
 * - Multiple sizes
 * - Header, body, footer sections
 * - Full ARIA support (dialog, labelledby, describedby)
 * - Keyboard navigation
 */

import {
  ReactNode,
  useEffect,
  useRef,
  MouseEvent,
  KeyboardEvent,
  forwardRef,
  useId,
} from 'react';
import { createPortal } from 'react-dom';

export interface ModalProps {
  /** Whether the modal is open */
  isOpen: boolean;

  /** Callback when modal should close */
  onClose: () => void;

  /** Modal title (required for accessibility) */
  title: string;

  /** Modal size */
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';

  /** Modal header content (overrides title if provided) */
  header?: ReactNode;

  /** Modal footer content */
  footer?: ReactNode;

  /** Whether clicking the backdrop closes the modal */
  closeOnBackdropClick?: boolean;

  /** Whether pressing Escape closes the modal */
  closeOnEscape?: boolean;

  /** Whether to show the close button */
  showCloseButton?: boolean;

  /** Additional CSS classes for the modal content */
  className?: string;

  /** Modal body content */
  children: ReactNode;
}

/**
 * Modal component with accessibility and focus management.
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 *
 * <Modal
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="Confirm Action"
 *   footer={
 *     <>
 *       <Button onClick={() => setIsOpen(false)}>Cancel</Button>
 *       <Button variant="primary" onClick={handleConfirm}>Confirm</Button>
 *     </>
 *   }
 * >
 *   <p>Are you sure you want to proceed?</p>
 * </Modal>
 * ```
 */
export const Modal = forwardRef<HTMLDivElement, ModalProps>(
  (
    {
      isOpen,
      onClose,
      title,
      size = 'md',
      header,
      footer,
      closeOnBackdropClick = true,
      closeOnEscape = true,
      showCloseButton = true,
      className = '',
      children,
    },
    ref
  ) => {
    const modalRef = useRef<HTMLDivElement>(null);
    const previousActiveElement = useRef<HTMLElement | null>(null);

    // Generate unique IDs for accessibility
    const titleId = useId();
    const descriptionId = useId();

    // Size styles
    const sizeStyles = {
      sm: 'max-w-sm',
      md: 'max-w-md',
      lg: 'max-w-lg',
      xl: 'max-w-xl',
      full: 'max-w-full mx-4',
    };

    // Handle body scroll lock
    useEffect(() => {
      if (isOpen) {
        // Save current active element
        previousActiveElement.current = document.activeElement as HTMLElement;

        // Lock body scroll
        document.body.style.overflow = 'hidden';

        // Focus the modal
        setTimeout(() => {
          modalRef.current?.focus();
        }, 0);

        return () => {
          // Restore body scroll
          document.body.style.overflow = '';

          // Restore focus to previous element
          previousActiveElement.current?.focus();
        };
      }
    }, [isOpen]);

    // Handle escape key
    useEffect(() => {
      if (!isOpen || !closeOnEscape) return;

      const handleEscape = (e: globalThis.KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }, [isOpen, closeOnEscape, onClose]);

    // Handle backdrop click
    const handleBackdropClick = (e: MouseEvent<HTMLDivElement>) => {
      if (closeOnBackdropClick && e.target === e.currentTarget) {
        onClose();
      }
    };

    // Focus trap - keep focus inside modal
    const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
      if (e.key !== 'Tab') return;

      const focusableElements = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (!focusableElements || focusableElements.length === 0) return;

      const firstElement = focusableElements[0] as HTMLElement;
      const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    };

    if (!isOpen) return null;

    const modalContent = (
      <div
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200"
        onClick={handleBackdropClick}
        aria-modal="true"
        role="dialog"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <div
          ref={modalRef}
          className={`relative bg-white rounded-lg shadow-xl w-full ${sizeStyles[size]} max-h-[90vh] overflow-hidden animate-in zoom-in-95 slide-in-from-bottom-4 duration-200 ${className}`}
          tabIndex={-1}
          onKeyDown={handleKeyDown}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            {header || (
              <h2
                id={titleId}
                className="text-xl font-bold text-gray-900"
              >
                {title}
              </h2>
            )}

            {showCloseButton && (
              <button
                type="button"
                onClick={onClose}
                className="ml-4 text-gray-400 hover:text-gray-600 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-lg p-1"
                aria-label="Close modal"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>

          {/* Body */}
          <div
            id={descriptionId}
            className="px-6 py-4 overflow-y-auto max-h-[calc(90vh-180px)]"
          >
            {children}
          </div>

          {/* Footer */}
          {footer && (
            <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
              {footer}
            </div>
          )}
        </div>
      </div>
    );

    // Render modal in a portal (outside the DOM hierarchy)
    return createPortal(modalContent, document.body);
  }
);

Modal.displayName = 'Modal';

export default Modal;
