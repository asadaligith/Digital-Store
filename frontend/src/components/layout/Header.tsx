/**
 * Header component with navigation, search, cart, and user menu.
 *
 * Features:
 * - Responsive design (mobile-first with hamburger menu)
 * - Logo and branding
 * - Navigation links
 * - Search bar
 * - Shopping cart with badge
 * - User account dropdown
 * - Sticky positioning
 * - ARIA navigation landmarks
 * - Mobile menu with slide animation
 */

import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../common/Button';
import { CartBadge } from '../cart/CartBadge';

export interface HeaderProps {
  /** Whether the header should stick to the top */
  sticky?: boolean;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Header component for site navigation and actions.
 *
 * @example
 * ```tsx
 * <Header sticky />
 * ```
 */
export const Header = ({ sticky = true, className = '' }: HeaderProps) => {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // TODO: Authentication state will come from auth context when implemented
  const isAuthenticated = false;
  const userName = 'John Doe';

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  // Navigation links
  const navLinks = [
    { label: 'Home', path: '/' },
    { label: 'Products', path: '/products' },
    { label: 'Categories', path: '/categories' },
    { label: 'Deals', path: '/deals' },
  ];

  // Position styles
  const positionStyles = sticky
    ? 'sticky top-0 z-40'
    : 'relative';

  return (
    <header
      className={`bg-white border-b border-gray-200 shadow-sm ${positionStyles} ${className}`}
      role="banner"
    >
      <nav
        className="container-custom"
        role="navigation"
        aria-label="Main navigation"
      >
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Link
              to="/"
              className="flex items-center space-x-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-lg px-2 py-1"
              aria-label="E-Commerce Store Home"
            >
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">E</span>
              </div>
              <span className="text-xl font-bold text-gray-900 hidden sm:inline">
                E-Commerce
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="px-4 py-2 text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Search Bar (Desktop) */}
          <div className="hidden lg:flex flex-1 max-w-md mx-6">
            <form onSubmit={handleSearch} className="w-full">
              <div className="relative">
                <input
                  type="search"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  aria-label="Search products"
                />
                <svg
                  className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </form>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Cart */}
            <CartBadge />

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="hidden md:block">
                <button
                  className="flex items-center space-x-2 p-2 text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                  aria-label="User menu"
                >
                  <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-semibold">
                      {userName.charAt(0)}
                    </span>
                  </div>
                  <span className="hidden lg:inline text-sm font-medium">
                    {userName.split(' ')[0]}
                  </span>
                </button>
              </div>
            ) : (
              <div className="hidden md:flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate('/login')}
                >
                  Sign In
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => navigate('/register')}
                >
                  Sign Up
                </Button>
              </div>
            )}

            {/* Mobile Menu Toggle */}
            <button
              type="button"
              onClick={toggleMobileMenu}
              className="md:hidden p-2 text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
              aria-label="Toggle mobile menu"
              aria-expanded={isMobileMenuOpen}
            >
              {isMobileMenuOpen ? (
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
              ) : (
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
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4 space-y-2">
            {/* Mobile Search */}
            <form onSubmit={handleSearch} className="px-2 mb-4">
              <div className="relative">
                <input
                  type="search"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="Search products"
                />
                <svg
                  className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
              </div>
            </form>

            {/* Mobile Navigation Links */}
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={closeMobileMenu}
                className="block px-4 py-3 text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors font-medium"
              >
                {link.label}
              </Link>
            ))}

            {/* Mobile Auth Buttons */}
            {!isAuthenticated && (
              <div className="px-2 pt-4 space-y-2 border-t border-gray-200">
                <Button
                  variant="outline"
                  fullWidth
                  onClick={() => {
                    navigate('/login');
                    closeMobileMenu();
                  }}
                >
                  Sign In
                </Button>
                <Button
                  variant="primary"
                  fullWidth
                  onClick={() => {
                    navigate('/register');
                    closeMobileMenu();
                  }}
                >
                  Sign Up
                </Button>
              </div>
            )}
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;
