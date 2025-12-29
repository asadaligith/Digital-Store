/**
 * Root application component with routing setup.
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CartProvider } from './contexts/CartContext';
import { CheckoutProvider } from './contexts/CheckoutContext';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import { Cart } from './pages/Cart';
import { Checkout } from './pages/Checkout';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

function App() {
  return (
    <BrowserRouter>
      <CartProvider>
        <CheckoutProvider>
          <Routes>
        {/* Home Page */}
        <Route
          path="/"
          element={
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Header />
              <main className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    Welcome to E-Commerce Store
                  </h1>
                  <p className="text-gray-600 mb-6">
                    Discover amazing products at great prices
                  </p>
                  <a
                    href="/products"
                    className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    Shop Now
                  </a>
                </div>
              </main>
              <Footer />
            </div>
          }
        />

        {/* Products Pages */}
        <Route path="/products" element={<Products />} />
        <Route path="/products/:slug" element={<ProductDetail />} />

        {/* Cart Page */}
        <Route path="/cart" element={<Cart />} />

        {/* Checkout Page */}
        <Route path="/checkout" element={<Checkout />} />

        {/* Catch-all 404 */}
        <Route
          path="*"
          element={
            <div className="min-h-screen bg-gray-50 flex flex-col">
              <Header />
              <main className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    404 - Page Not Found
                  </h1>
                  <p className="text-gray-600 mb-6">
                    The page you are looking for does not exist.
                  </p>
                  <a
                    href="/"
                    className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    Go Home
                  </a>
                </div>
              </main>
              <Footer />
            </div>
          }
        />
      </Routes>
        </CheckoutProvider>
      </CartProvider>
    </BrowserRouter>
  );
}

export default App;
