# Tasks: E-Commerce Store Platform

**Input**: Design documents from `/specs/001-ecommerce-store/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as per constitutional TDD requirements (>80% coverage for business logic)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below use web app structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create monorepo directory structure (frontend/ and backend/ directories)
- [ ] T002 [P] Initialize frontend with Vite + React + TypeScript in frontend/
- [ ] T003 [P] Initialize backend with FastAPI + Python in backend/
- [ ] T004 [P] Create frontend/package.json with dependencies (React 18.2+, Vite 5+, Tailwind CSS 3.4+, GSAP 3.12+, React Router 6+, Axios 1+, Vitest, React Testing Library, Playwright)
- [ ] T005 [P] Create backend/requirements.txt with dependencies (FastAPI 0.104+, Motor 3+, Pydantic 2+, PyJWT 2+, bcrypt, python-dotenv, pytest, httpx)
- [ ] T006 [P] Configure Tailwind CSS in frontend/tailwind.config.js with mobile-first breakpoints (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)
- [ ] T007 [P] Configure TypeScript in frontend/tsconfig.json with strict mode enabled
- [ ] T008 [P] Configure ESLint in frontend/.eslintrc.js
- [ ] T009 [P] Configure Prettier in frontend/.prettierrc
- [ ] T010 [P] Configure Black and Ruff in backend/pyproject.toml
- [ ] T011 [P] Configure mypy for Python type checking in backend/pyproject.toml
- [ ] T012 Create docker-compose.yml for MongoDB 7+ service
- [ ] T013 Create frontend/.env.example with environment variables (VITE_API_BASE_URL, VITE_STRIPE_PUBLISHABLE_KEY, VITE_ENVIRONMENT)
- [ ] T014 Create backend/.env.example with environment variables (MONGODB_URI, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, STRIPE_SECRET_KEY, SENDGRID_API_KEY, CLOUDINARY_API_KEY, CORS_ORIGINS)
- [ ] T015 [P] Create .gitignore files for frontend and backend
- [ ] T016 Create pre-commit hooks configuration in .pre-commit-config.yaml (Black, Ruff, Prettier, ESLint)
- [ ] T017 [P] Create frontend/README.md with setup instructions
- [ ] T018 [P] Create backend/README.md with setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T019 Create MongoDB client setup in backend/src/db/mongodb.py with Motor async driver and connection pooling (max_pool_size=50, min_pool_size=10)
- [ ] T020 Create database index creation script in backend/src/db/indexes.py (users.email unique, products.slug unique, products.sku unique, orders.order_number unique, carts.user_id unique sparse)
- [ ] T021 Create core configuration in backend/src/core/config.py using Pydantic BaseSettings for environment variable validation
- [ ] T022 Create JWT security utilities in backend/src/core/security.py (generate_access_token, generate_refresh_token, verify_token, hash_password, verify_password using bcrypt ≥12 rounds)
- [ ] T023 Create custom exceptions in backend/src/core/exceptions.py (UnauthorizedException, NotFoundException, ValidationException, DuplicateException)
- [ ] T024 Create CORS middleware in backend/src/api/middleware/cors.py with CORS whitelist from environment
- [ ] T025 Create error handling middleware in backend/src/api/middleware/error_handler.py (catch exceptions, return structured error responses, hide stack traces in production)
- [ ] T026 Create structured logging middleware in backend/src/api/middleware/logger.py (JSON format logs with request ID, method, path, status, duration)
- [ ] T027 Create JWT authentication dependency in backend/src/api/dependencies/auth.py (get_current_user, get_current_active_user extracting user from JWT token)
- [ ] T028 Create rate limiting dependency in backend/src/api/dependencies/rate_limit.py (100 req/min for authenticated, 20 req/min for anonymous using slowapi)
- [ ] T029 Create FastAPI app initialization in backend/src/main.py (register routers, middleware, startup/shutdown events for MongoDB connection)
- [ ] T030 [P] Create base Axios client in frontend/src/services/api/client.ts with interceptors for JWT tokens, error handling, and request/response transformation
- [ ] T031 [P] Create global TypeScript types in frontend/src/types/api.ts (ApiResponse, ApiError, PaginationMeta)
- [ ] T032 [P] Create global CSS with Tailwind imports in frontend/src/styles/index.css
- [ ] T033 [P] Create App.tsx with React Router setup (BrowserRouter, Routes, Route placeholders)
- [ ] T034 [P] Create main.tsx entry point with React.StrictMode and App component
- [ ] T035 [P] Create common Button component in frontend/src/components/common/Button.tsx with TypeScript interface, Tailwind styles, touch target ≥44px, keyboard navigation, ARIA labels
- [ ] T036 [P] Create common Input component in frontend/src/components/common/Input.tsx with TypeScript interface, validation states, error messages, ARIA labels
- [ ] T037 [P] Create common Card component in frontend/src/components/common/Card.tsx with TypeScript interface, responsive padding
- [ ] T038 [P] Create common Modal component in frontend/src/components/common/Modal.tsx with TypeScript interface, focus trap, Escape key close, ARIA dialog
- [ ] T039 [P] Create common Spinner component in frontend/src/components/common/Spinner.tsx with GSAP rotation animation (infinite, linear)
- [ ] T040 [P] Create Header component in frontend/src/components/layout/Header.tsx with logo, navigation links, cart icon placeholder, mobile menu toggle
- [ ] T041 [P] Create Footer component in frontend/src/components/layout/Footer.tsx with copyright, links, responsive layout
- [ ] T042 [P] Create useAnimations custom hook in frontend/src/hooks/useAnimations.ts with GSAP cleanup utility (returns gsap instance and cleanup function)
- [ ] T043 Create seed data script in backend/src/scripts/seed_data.py (create 10 categories, 100 sample products, 5 test users with verified emails)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Browse and Discover Products (Priority: P1) 🎯 MVP

**Goal**: Implement product discovery features (homepage, product listing, filters, search, product details)

**Independent Test**: Load homepage → navigate to product listings → apply filters/search → view product details

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T044 [P] [US1] Create product service unit tests in backend/tests/unit/test_product_service.py (test list_products, get_product_by_id, get_product_by_slug, search_products, filter_products with mocked repository)
- [ ] T045 [P] [US1] Create product API integration tests in backend/tests/integration/test_products_api.py (test GET /api/products with filters, pagination, sorting; test GET /api/products/:id; test GET /api/categories)
- [ ] T046 [P] [US1] Create ProductCard component tests in frontend/tests/component/ProductCard.test.tsx (render product info, Add to Cart button click, image display, rating display)
- [ ] T047 [P] [US1] Create ProductGrid component tests in frontend/tests/component/ProductGrid.test.tsx (render products in grid, responsive breakpoints, loading state, empty state)
- [ ] T048 [P] [US1] Create useProducts hook tests in frontend/tests/unit/useProducts.test.ts (fetch products, apply filters, pagination, loading states, error handling)
- [ ] T049 [US1] Create E2E test for browse flow in frontend/tests/e2e/browse-products.spec.ts (homepage → product listing → filter → search → product detail using Playwright)

### Implementation for User Story 1

**Backend**:

- [ ] T050 [P] [US1] Create Product Pydantic model in backend/src/models/product.py (id, name, slug, description, specifications dict, price Decimal128, category_id, brand, sku, stock_quantity, is_available, images array, average_rating, review_count, created_at, updated_at)
- [ ] T051 [P] [US1] Create Category Pydantic model in backend/src/models/category.py (id, name, slug, parent_id optional, description, image_url, display_order, is_active)
- [ ] T052 [P] [US1] Create ProductRepository in backend/src/repositories/product_repository.py (find_all with filters/pagination/sorting, find_by_id, find_by_slug, search_by_text, count_all with filters using Motor async)
- [ ] T053 [P] [US1] Create CategoryRepository in backend/src/repositories/category_repository.py (find_all, find_by_id, find_by_slug using Motor async)
- [ ] T054 [US1] Create ProductService in backend/src/services/product_service.py (list_products with pagination/filters/sorting, get_product_by_id, get_product_by_slug, search_products business logic, calculate_average_rating)
- [ ] T055 [US1] Create CategoryService in backend/src/services/category_service.py (list_categories, get_category_hierarchy business logic)
- [ ] T056 [US1] Create product API routes in backend/src/api/routes/products.py (GET /api/products with query params for filters/pagination/sorting, GET /api/products/:id, GET /api/categories)

**Frontend**:

- [ ] T057 [P] [US1] Create Product TypeScript types in frontend/src/types/product.ts (Product interface, Category interface, ProductFilters interface, ProductListResponse interface)
- [ ] T058 [P] [US1] Create products API client in frontend/src/services/api/products.ts (fetchProducts, fetchProductById, fetchCategories using Axios with type-safe interfaces)
- [ ] T059 [P] [US1] Create useProducts custom hook in frontend/src/hooks/useProducts.ts (fetch products, apply filters, pagination, sorting, loading/error states using React Query or useState)
- [ ] T060 [P] [US1] Create ProductCard component in frontend/src/components/products/ProductCard.tsx (responsive card with image, name, price, rating, Add to Cart button, hover animation with GSAP scale/y-transform, mobile-first design 320px→768px→1024px)
- [ ] T061 [P] [US1] Create ProductGrid component in frontend/src/components/products/ProductGrid.tsx (responsive grid layout using Tailwind grid, loading skeleton, empty state, grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4)
- [ ] T062 [P] [US1] Create SearchBar component in frontend/src/components/products/SearchBar.tsx (input with search icon, real-time suggestions dropdown, debounced search, keyboard navigation, ARIA combobox)
- [ ] T063 [P] [US1] Create FilterPanel component in frontend/src/components/products/FilterPanel.tsx (category filter, price range slider, rating filter, availability checkbox, mobile drawer/desktop sidebar responsive layout)
- [ ] T064 [P] [US1] Create ProductImageGallery component in frontend/src/components/products/ProductImageGallery.tsx (main image display, thumbnail carousel, zoom on click modal, GSAP fade transition between images, responsive srcset)
- [ ] T065 [P] [US1] Create ProductDetail component in frontend/src/components/products/ProductDetail.tsx (images, name, price, description, specifications, reviews, Add to Cart form, stock status, breadcrumbs)
- [ ] T066 [US1] Create HomePage in frontend/src/pages/HomePage.tsx (hero banner with GSAP fade-in animation, featured products grid, category cards, promotional sections, page fade-in animation on mount)
- [ ] T067 [US1] Create ProductListPage in frontend/src/pages/ProductListPage.tsx (SearchBar, FilterPanel, ProductGrid, pagination/infinite scroll, sort dropdown, active filters display, URL query params sync)
- [ ] T068 [US1] Create ProductDetailPage in frontend/src/pages/ProductDetailPage.tsx (ProductImageGallery, ProductDetail, reviews section, related products, breadcrumb navigation, page fade-in animation)
- [ ] T069 [US1] Add routes to App.tsx (/ for HomePage, /products for ProductListPage, /products/:slug for ProductDetailPage)
- [ ] T070 [US1] Add GSAP page transition animations (fade in on route change, cleanup on unmount using useEffect and gsap.timeline)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add Products to Shopping Cart (Priority: P2)

**Goal**: Implement shopping cart functionality (add to cart, update quantity, remove item, view cart)

**Independent Test**: Add products to cart → view cart page → modify quantities → remove items → see updated totals

### Tests for User Story 2 ⚠️

- [ ] T071 [P] [US2] Create cart service unit tests in backend/tests/unit/test_cart_service.py (test get_or_create_cart, add_item, update_quantity, remove_item, calculate_totals with mocked repository)
- [ ] T072 [P] [US2] Create cart API integration tests in backend/tests/integration/test_cart_api.py (test GET /api/cart, POST /api/cart/items, PATCH /api/cart/items/:id, DELETE /api/cart/items/:id)
- [ ] T073 [P] [US2] Create useCart hook tests in frontend/tests/unit/useCart.test.ts (add to cart, update quantity, remove item, cart sync with backend, localStorage persistence for guests)
- [ ] T074 [P] [US2] Create CartItem component tests in frontend/tests/component/CartItem.test.tsx (render item info, quantity selector, remove button, subtotal calculation)
- [ ] T075 [US2] Create E2E test for cart flow in frontend/tests/e2e/shopping-cart.spec.ts (add item from product detail → view cart → update quantity → remove item → totals update using Playwright)

### Implementation for User Story 2

**Backend**:

- [ ] T076 [P] [US2] Create Cart Pydantic model in backend/src/models/cart.py (id, user_id optional, session_id optional, items array with embedded CartItem, created_at, updated_at, expires_at for guest carts)
- [ ] T077 [P] [US2] Create CartItem embedded model in backend/src/models/cart.py (product_id, quantity min 1 max 99, price_at_addition Decimal128, added_at)
- [ ] T078 [P] [US2] Create CartRepository in backend/src/repositories/cart_repository.py (find_by_user_id, find_by_session_id, create_cart, add_item using find_one_and_update atomic, update_item_quantity, remove_item, clear_cart using Motor async)
- [ ] T079 [US2] Create CartService in backend/src/services/cart_service.py (get_or_create_cart for user/guest, add_item with stock validation, update_quantity, remove_item, calculate_subtotal, calculate_totals business logic, handle cart expiration)
- [ ] T080 [US2] Create cart API routes in backend/src/api/routes/cart.py (GET /api/cart, POST /api/cart/items, PATCH /api/cart/items/:product_id, DELETE /api/cart/items/:product_id, DELETE /api/cart clear cart)

**Frontend**:

- [ ] T081 [P] [US2] Create Cart TypeScript types in frontend/src/types/cart.ts (Cart interface, CartItem interface, AddToCartRequest interface, UpdateCartItemRequest interface)
- [ ] T082 [P] [US2] Create cart API client in frontend/src/services/api/cart.ts (fetchCart, addItem, updateItem, removeItem, clearCart using Axios)
- [ ] T083 [P] [US2] Create localStorage utility in frontend/src/services/storage/localStorage.ts (getCart, setCart, clearCart, mergeCart functions with 7-day expiry timestamp)
- [ ] T084 [US2] Create CartContext in frontend/src/contexts/CartContext.tsx (cart state, add to cart, update quantity, remove item, clear cart, sync with backend for authenticated users, localStorage for guests, cart item count)
- [ ] T085 [US2] Create useCart custom hook in frontend/src/hooks/useCart.ts (access CartContext, provide cart actions and state)
- [ ] T086 [P] [US2] Create CartIcon component in frontend/src/components/cart/CartIcon.tsx (shopping cart icon SVG, item count badge, click to navigate to cart page, bounce animation on add using GSAP scale timeline)
- [ ] T087 [P] [US2] Create CartItem component in frontend/src/components/cart/CartItem.tsx (product image, name link to product detail, price, quantity selector with +/- buttons, subtotal, remove button, fade-out animation on remove using GSAP x/opacity)
- [ ] T088 [P] [US2] Create CartSummary component in frontend/src/components/cart/CartSummary.tsx (subtotal, estimated tax, estimated shipping, total, Proceed to Checkout button, responsive layout)
- [ ] T089 [US2] Create CartPage in frontend/src/pages/CartPage.tsx (list of CartItem components, CartSummary, empty cart state with Continue Shopping link, page fade-in animation)
- [ ] T090 [US2] Add CartIcon to Header component in frontend/src/components/layout/Header.tsx (position in top right, visible on all pages)
- [ ] T091 [US2] Wrap App.tsx with CartContext provider
- [ ] T092 [US2] Add /cart route to App.tsx for CartPage
- [ ] T093 [US2] Add cart merge logic on user login (merge localStorage cart with backend cart, deduplicate by product_id using max quantity)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: User Story 3 - Complete Checkout Process (Priority: P3)

**Goal**: Implement checkout flow (shipping info, shipping method, order review)

**Independent Test**: Start with pre-filled cart → enter shipping details → select shipping method → review order summary

### Tests for User Story 3 ⚠️

- [ ] T094 [P] [US3] Create checkout service unit tests in backend/tests/unit/test_checkout_service.py (test validate_cart, calculate_shipping, calculate_tax, create_order_preview with mocked repositories)
- [ ] T095 [P] [US3] Create checkout API integration tests in backend/tests/integration/test_checkout_api.py (test POST /api/checkout/validate, POST /api/checkout/calculate-shipping)
- [ ] T096 [P] [US3] Create useCheckout hook tests in frontend/tests/unit/useCheckout.test.ts (multi-step wizard state management, form validation, total calculations)
- [ ] T097 [P] [US3] Create ShippingForm component tests in frontend/tests/component/ShippingForm.test.tsx (form validation, error messages, required fields, React Hook Form integration)
- [ ] T098 [US3] Create E2E test for checkout flow in frontend/tests/e2e/checkout-process.spec.ts (guest checkout → shipping info → shipping method → review order using Playwright)

### Implementation for User Story 3

**Backend**:

- [ ] T099 [P] [US3] Create Address Pydantic model in backend/src/models/address.py (id, user_id optional, type enum shipping/billing/both, full_name, address_line1, address_line2 optional, city, state, postal_code, country, phone, is_default boolean)
- [ ] T100 [P] [US3] Create ShippingMethod Pydantic model in backend/src/models/checkout.py (method enum standard/express/overnight, cost Decimal128, estimated_days int)
- [ ] T101 [P] [US3] Create CheckoutRepository in backend/src/repositories/checkout_repository.py (validate_cart_items_stock, get_shipping_methods using Motor async)
- [ ] T102 [US3] Create CheckoutService in backend/src/services/checkout_service.py (validate_cart business logic, calculate_shipping_cost based on method, calculate_tax based on address, create_order_preview with totals)
- [ ] T103 [US3] Create checkout API routes in backend/src/api/routes/checkout.py (POST /api/checkout/validate, POST /api/checkout/calculate-shipping with shipping address and method)

**Frontend**:

- [ ] T104 [P] [US3] Create Address TypeScript types in frontend/src/types/address.ts (Address interface, ShippingMethod interface, CheckoutStep enum)
- [ ] T105 [P] [US3] Create checkout API client in frontend/src/services/api/checkout.ts (validateCart, calculateShipping using Axios)
- [ ] T106 [P] [US3] Create address validation utilities in frontend/src/utils/validation.ts (validateEmail, validatePhone, validatePostalCode using Zod schemas)
- [ ] T107 [US3] Create CheckoutContext in frontend/src/contexts/CheckoutContext.tsx (current step, shipping address, shipping method, totals, next step, previous step, update shipping address, update shipping method)
- [ ] T108 [US3] Create useCheckout custom hook in frontend/src/hooks/useCheckout.ts (access CheckoutContext, provide checkout actions and state)
- [ ] T109 [P] [US3] Create ShippingForm component in frontend/src/components/checkout/ShippingForm.tsx (React Hook Form with Zod validation, full_name, address_line1, address_line2, city, state, postal_code, country, phone fields, error messages, ARIA labels, Continue button)
- [ ] T110 [P] [US3] Create ShippingMethodSelector component in frontend/src/components/checkout/ShippingMethodSelector.tsx (radio button group for standard/express/overnight, display cost and estimated delivery, responsive card layout, Continue button)
- [ ] T111 [P] [US3] Create OrderReview component in frontend/src/components/checkout/OrderReview.tsx (order items list, shipping address display, shipping method display, subtotal/shipping/tax/total breakdown, Edit Address button, Confirm Order button)
- [ ] T112 [P] [US3] Create CheckoutSteps component in frontend/src/components/checkout/CheckoutSteps.tsx (progress indicator showing Shipping Info → Shipping Method → Review → Payment, highlight current step, mobile-first responsive)
- [ ] T113 [US3] Create CheckoutPage in frontend/src/pages/CheckoutPage.tsx (CheckoutSteps, conditional render based on current step: ShippingForm/ShippingMethodSelector/OrderReview, guest checkout support, redirect to login modal with continue as guest option, GSAP step transition animations using x/opacity)
- [ ] T114 [US3] Wrap App.tsx with CheckoutContext provider
- [ ] T115 [US3] Add /checkout route to App.tsx for CheckoutPage
- [ ] T116 [US3] Add Proceed to Checkout button navigation in CartSummary component (navigate to /checkout)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Complete Payment (Priority: P4)

**Goal**: Implement payment processing and order confirmation (Stripe integration, order creation, email confirmation)

**Independent Test**: Start with confirmed order → enter payment info → process payment → view order confirmation

### Tests for User Story 4 ⚠️

- [ ] T117 [P] [US4] Create order service unit tests in backend/tests/unit/test_order_service.py (test create_order, generate_order_number, update_order_status with mocked repositories)
- [ ] T118 [P] [US4] Create payment service unit tests in backend/tests/unit/test_payment_service.py (test create_payment_intent, confirm_payment, handle_webhook with mocked Stripe SDK)
- [ ] T119 [P] [US4] Create order API integration tests in backend/tests/integration/test_orders_api.py (test POST /api/orders, GET /api/orders, GET /api/orders/:id)
- [ ] T120 [P] [US4] Create payment API integration tests in backend/tests/integration/test_payments_api.py (test POST /api/payments/process, POST /api/payments/webhook with mocked Stripe)
- [ ] T121 [US4] Create E2E test for payment flow in frontend/tests/e2e/payment-process.spec.ts (enter payment info → process → confirmation page using Playwright with Stripe test card 4242424242424242)

### Implementation for User Story 4

**Backend**:

- [ ] T122 [P] [US4] Create Order Pydantic model in backend/src/models/order.py (id, order_number, user_id optional, guest_email optional, status enum pending/processing/shipped/delivered/cancelled, items array with embedded OrderItem, shipping_address embedded Address, shipping_method, shipping_cost, subtotal, tax_amount, total_amount, payment_id, estimated_delivery_date, tracking_number optional, notes optional, created_at, updated_at, shipped_at, delivered_at, cancelled_at)
- [ ] T123 [P] [US4] Create OrderItem embedded model in backend/src/models/order.py (product_id, product_name denormalized, product_sku denormalized, quantity, price_at_purchase denormalized Decimal128, subtotal)
- [ ] T124 [P] [US4] Create Payment Pydantic model in backend/src/models/payment.py (id, order_id, payment_method enum credit_card/debit_card/paypal/apple_pay/google_pay, payment_provider stripe/paypal, transaction_id, status enum pending/completed/failed/refunded, amount Decimal128, currency USD, card_last4 optional, card_brand optional, failure_reason optional, refund_amount optional, refund_reason optional, metadata dict, created_at, completed_at, failed_at, refunded_at)
- [ ] T125 [P] [US4] Create OrderRepository in backend/src/repositories/order_repository.py (create_order, find_by_id, find_by_order_number, find_by_user_id with pagination, update_status using Motor async)
- [ ] T126 [P] [US4] Create PaymentRepository in backend/src/repositories/payment_repository.py (create_payment, find_by_order_id, find_by_transaction_id, update_status using Motor async)
- [ ] T127 [US4] Create OrderService in backend/src/services/order_service.py (create_order_from_cart business logic, generate_order_number format ORD-YYYYMMDD-XXXXXX, validate_inventory_before_order, update_inventory_after_order, calculate_estimated_delivery_date)
- [ ] T128 [US4] Create PaymentService in backend/src/services/payment_service.py (create_stripe_payment_intent, confirm_payment, handle_stripe_webhook, verify_webhook_signature, process_successful_payment, process_failed_payment, create_payment_record)
- [ ] T129 [US4] Create EmailService in backend/src/services/email_service.py (send_order_confirmation_email using SendGrid with order details, send_email_verification, send_password_reset_email)
- [ ] T130 [US4] Create order API routes in backend/src/api/routes/orders.py (POST /api/orders create order and initiate payment, GET /api/orders list user orders with pagination, GET /api/orders/:id get order details, requires authentication)
- [ ] T131 [US4] Create payment API routes in backend/src/api/routes/payments.py (POST /api/payments/process process payment with Stripe, POST /api/payments/webhook handle Stripe webhook callbacks)
- [ ] T132 [US4] Create webhook signature verification in payment routes (verify Stripe webhook signature using STRIPE_WEBHOOK_SECRET)

**Frontend**:

- [ ] T133 [P] [US4] Create Order TypeScript types in frontend/src/types/order.ts (Order interface, OrderItem interface, CreateOrderRequest interface, OrderStatus enum)
- [ ] T134 [P] [US4] Create Payment TypeScript types in frontend/src/types/payment.ts (PaymentMethod enum, PaymentIntent interface, PaymentStatus enum)
- [ ] T135 [P] [US4] Create orders API client in frontend/src/services/api/orders.ts (createOrder, fetchOrders, fetchOrderById using Axios)
- [ ] T136 [P] [US4] Create payments API client in frontend/src/services/api/payments.ts (processPayment using Axios)
- [ ] T137 [P] [US4] Install Stripe dependencies (@stripe/stripe-js, @stripe/react-stripe-js) in frontend/package.json
- [ ] T138 [P] [US4] Create Stripe Elements wrapper in frontend/src/components/checkout/StripeElements.tsx (Elements provider with Stripe public key from environment, appearance customization)
- [ ] T139 [P] [US4] Create PaymentForm component in frontend/src/components/checkout/PaymentForm.tsx (Stripe CardElement, billing address optional, payment method selector radio buttons, Pay Now button, loading state with spinner, error message display, 3D Secure support)
- [ ] T140 [P] [US4] Create OrderConfirmation component in frontend/src/components/checkout/OrderConfirmation.tsx (success icon with GSAP scale animation, order number display, order summary, estimated delivery date, email confirmation notice, Continue Shopping button, View Order Details button, confetti animation using GSAP stagger)
- [ ] T141 [US4] Create PaymentPage in frontend/src/pages/PaymentPage.tsx (wrap PaymentForm with StripeElements, order summary sidebar, secure checkout badge, payment processing loader with GSAP rotation, error handling with shake animation)
- [ ] T142 [US4] Create OrderConfirmationPage in frontend/src/pages/OrderConfirmationPage.tsx (OrderConfirmation component, prevent duplicate order creation on refresh by checking order status, page fade-in animation)
- [ ] T143 [US4] Add /payment route to App.tsx for PaymentPage
- [ ] T144 [US4] Add /order-confirmation/:orderId route to App.tsx for OrderConfirmationPage
- [ ] T145 [US4] Add Confirm Order button navigation in OrderReview component (navigate to /payment)
- [ ] T146 [US4] Implement payment flow in PaymentPage (create PaymentIntent, confirm payment, handle success/failure, navigate to confirmation on success)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - User Account Management (Priority: P5)

**Goal**: Implement user registration, login, profile, order history, saved addresses

**Independent Test**: Register account → verify email → login → view profile → manage addresses → view order history

### Tests for User Story 5 ⚠️

- [ ] T147 [P] [US5] Create auth service unit tests in backend/tests/unit/test_auth_service.py (test register, login, verify_email, forgot_password, reset_password, generate_jwt, verify_jwt with mocked repository)
- [ ] T148 [P] [US5] Create user service unit tests in backend/tests/unit/test_user_service.py (test get_profile, update_profile, add_address, update_address, delete_address with mocked repository)
- [ ] T149 [P] [US5] Create auth API integration tests in backend/tests/integration/test_auth_api.py (test POST /api/auth/register, POST /api/auth/login, POST /api/auth/logout, POST /api/auth/refresh, POST /api/auth/forgot-password, POST /api/auth/reset-password)
- [ ] T150 [P] [US5] Create user API integration tests in backend/tests/integration/test_users_api.py (test GET /api/users/profile, PATCH /api/users/profile, GET /api/users/addresses, POST /api/users/addresses, PATCH /api/users/addresses/:id, DELETE /api/users/addresses/:id, GET /api/users/orders)
- [ ] T151 [P] [US5] Create useAuth hook tests in frontend/tests/unit/useAuth.test.ts (register, login, logout, token refresh, check auth status)
- [ ] T152 [US5] Create E2E test for account flow in frontend/tests/e2e/user-account.spec.ts (register → verify email → login → view profile → view orders using Playwright)

### Implementation for User Story 5

**Backend**:

- [ ] T153 [P] [US5] Create User Pydantic model in backend/src/models/user.py (id, email unique EmailStr, password_hash, full_name, phone optional, is_email_verified boolean default false, verification_token optional, reset_token optional, reset_token_expiry optional, failed_login_attempts int default 0, lockout_until optional, created_at, updated_at, last_login_at optional)
- [ ] T154 [P] [US5] Create RefreshToken Pydantic model in backend/src/models/refresh_token.py (id, user_id, token hashed UUID, expires_at 7 days from creation, created_at, is_revoked boolean default false)
- [ ] T155 [P] [US5] Create UserRepository in backend/src/repositories/user_repository.py (create_user, find_by_email, find_by_id, update_user, update_verification_status, update_password, increment_failed_login_attempts, reset_failed_login_attempts, set_lockout using Motor async)
- [ ] T156 [P] [US5] Create RefreshTokenRepository in backend/src/repositories/refresh_token_repository.py (create_token, find_by_token, revoke_token, revoke_all_user_tokens, delete_expired_tokens using Motor async)
- [ ] T157 [P] [US5] Create AddressRepository in backend/src/repositories/address_repository.py (create_address, find_by_user_id, find_by_id, update_address, delete_address, set_default_address unset others using Motor async)
- [ ] T158 [US5] Create AuthService in backend/src/services/auth_service.py (register user with bcrypt ≥12 rounds, login with password verification and lockout logic, generate_verification_token, verify_email_token, generate_reset_token, reset_password, generate_access_token 15min expiry, generate_refresh_token 7 days expiry, refresh_access_token with token rotation, logout revoke refresh token)
- [ ] T159 [US5] Create UserService in backend/src/services/user_service.py (get_profile, update_profile, add_address, update_address, delete_address, set_default_address, get_user_orders business logic)
- [ ] T160 [US5] Create auth API routes in backend/src/api/routes/auth.py (POST /api/auth/register, POST /api/auth/login set httpOnly cookies, POST /api/auth/logout, POST /api/auth/refresh, POST /api/auth/forgot-password, POST /api/auth/reset-password, POST /api/auth/verify-email)
- [ ] T161 [US5] Create user API routes in backend/src/api/routes/users.py (GET /api/users/profile, PATCH /api/users/profile, GET /api/users/addresses, POST /api/users/addresses, PATCH /api/users/addresses/:id, DELETE /api/users/addresses/:id, GET /api/users/orders with pagination, all require authentication)
- [ ] T162 [US5] Add rate limiting to auth routes (5 failed attempts → 15-minute lockout)

**Frontend**:

- [ ] T163 [P] [US5] Create User TypeScript types in frontend/src/types/user.ts (User interface, RegisterRequest interface, LoginRequest interface, UpdateProfileRequest interface)
- [ ] T164 [P] [US5] Create auth API client in frontend/src/services/api/auth.ts (register, login, logout, refresh, forgotPassword, resetPassword, verifyEmail using Axios)
- [ ] T165 [P] [US5] Create users API client in frontend/src/services/api/users.ts (fetchProfile, updateProfile, fetchAddresses, addAddress, updateAddress, deleteAddress, fetchOrders using Axios)
- [ ] T166 [US5] Create AuthContext in frontend/src/contexts/AuthContext.tsx (user state, token state, isAuthenticated boolean, login, logout, register, checkAuthStatus, refresh token automatically before expiry using setInterval)
- [ ] T167 [US5] Create useAuth custom hook in frontend/src/hooks/useAuth.ts (access AuthContext, provide auth actions and state)
- [ ] T168 [P] [US5] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx (React Hook Form with Zod validation, email and password fields, remember me checkbox, submit button, forgot password link, error message display, ARIA labels)
- [ ] T169 [P] [US5] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx (React Hook Form with Zod validation, email, password with strength indicator, confirm password, full_name, phone optional, submit button, email verification notice after signup, ARIA labels)
- [ ] T170 [P] [US5] Create ProtectedRoute component in frontend/src/components/auth/ProtectedRoute.tsx (check isAuthenticated, redirect to /login if not authenticated, preserve intended destination in returnUrl query param)
- [ ] T171 [P] [US5] Create ProfileInfo component in frontend/src/components/auth/ProfileInfo.tsx (display user email, full_name, phone, created_at, edit profile button)
- [ ] T172 [P] [US5] Create SavedAddressesList component in frontend/src/components/auth/SavedAddressesList.tsx (list of addresses with edit/delete/set default buttons, add new address button, responsive card layout)
- [ ] T173 [P] [US5] Create OrderHistoryList component in frontend/src/components/auth/OrderHistoryList.tsx (list of orders with order number, date, status, total, view details button, pagination, status badge colors, responsive table/card layout)
- [ ] T174 [US5] Create LoginPage in frontend/src/pages/LoginPage.tsx (LoginForm component, sign up link, page fade-in animation)
- [ ] T175 [US5] Create SignupPage in frontend/src/pages/SignupPage.tsx (SignupForm component, login link, page fade-in animation)
- [ ] T176 [US5] Create AccountDashboardPage in frontend/src/pages/AccountDashboardPage.tsx (ProfileInfo, SavedAddressesList, OrderHistoryList in tabs or sections, page fade-in animation, protected route)
- [ ] T177 [US5] Create OrderDetailPage in frontend/src/pages/OrderDetailPage.tsx (order number, status, items, shipping address, payment method, totals, tracking number if shipped, estimated delivery, page fade-in animation, protected route)
- [ ] T178 [US5] Wrap App.tsx with AuthContext provider (top-level, before CartContext)
- [ ] T179 [US5] Add /login route to App.tsx for LoginPage
- [ ] T180 [US5] Add /signup route to App.tsx for SignupPage
- [ ] T181 [US5] Add /account route to App.tsx for AccountDashboardPage with ProtectedRoute
- [ ] T182 [US5] Add /orders/:orderId route to App.tsx for OrderDetailPage with ProtectedRoute
- [ ] T183 [US5] Add user menu to Header component (login/signup links when not authenticated, account dropdown with logout when authenticated)
- [ ] T184 [US5] Add token refresh interceptor to Axios client (refresh token when 401 received, retry failed request with new token)

**Checkpoint**: All user stories should now be fully functional and independently testable

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, performance optimization, production readiness

- [ ] T185 [P] Implement code splitting for routes using React.lazy() and Suspense (HomePage, ProductListPage, ProductDetailPage, CartPage, CheckoutPage, PaymentPage, AccountDashboardPage lazy loaded)
- [ ] T186 [P] Optimize images for WebP format with responsive srcset in ProductCard and ProductImageGallery components
- [ ] T187 [P] Implement lazy loading for below-fold images using loading="lazy" attribute
- [ ] T188 [P] Add Intersection Observer for infinite scroll pagination in ProductListPage (replace or complement pagination)
- [ ] T189 [P] Create GSAP animation utility functions in frontend/src/utils/animations.ts (fadeIn, fadeOut, slideIn, slideOut, scaleUp, bounce reusable timeline creators)
- [ ] T190 [P] Implement prefers-reduced-motion media query support in useAnimations hook (detect and skip animations if user prefers reduced motion)
- [ ] T191 [P] Add focus management for modal dialogs and route changes (restore focus on close, focus first input on modal open)
- [ ] T192 [P] Run axe DevTools accessibility audit and fix violations (color contrast, ARIA labels, keyboard navigation, focus indicators)
- [ ] T193 [P] Test with NVDA screen reader (Windows) or VoiceOver (Mac) and fix screen reader issues
- [ ] T194 [P] Create custom 404 NotFoundPage in frontend/src/pages/NotFoundPage.tsx with link to homepage
- [ ] T195 [P] Create ErrorBoundary component in frontend/src/components/common/ErrorBoundary.tsx (catch React errors, display fallback UI, log to Sentry or console)
- [ ] T196 [P] Add error tracking with Sentry in frontend/src/main.tsx (Sentry.init with DSN from environment)
- [ ] T197 [P] Implement API response caching in backend using Redis or in-memory cache (cache product catalog, categories for 5-10 minutes)
- [ ] T198 [P] Add database query optimization (ensure all indexes created, use explain() to verify query performance, add missing indexes)
- [ ] T199 [P] Create API documentation with Swagger UI in backend/src/main.py (use FastAPI's built-in OpenAPI, add descriptions to endpoints, add example request/response)
- [ ] T200 [P] Create frontend environment validation in frontend/src/main.tsx (check required env vars on startup, throw error if missing)
- [ ] T201 [P] Create backend environment validation in backend/src/core/config.py (validate all required env vars using Pydantic, throw error on startup if missing)
- [ ] T202 [P] Add security headers middleware in backend/src/api/middleware/security.py (CSP, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security)
- [ ] T203 [P] Implement CSRF token generation and validation in backend/src/core/security.py and backend/src/api/middleware/csrf.py
- [ ] T204 [P] Create bundle size analysis script in frontend/package.json (vite-bundle-visualizer, run and verify <200KB gzipped main bundle)
- [ ] T205 [P] Add performance monitoring to measure FCP, LCP, TTI, CLS using web-vitals library in frontend/src/utils/performance.ts
- [ ] T206 [P] Create database cleanup job script in backend/src/scripts/cleanup.py (delete expired guest carts, expired verification tokens, expired refresh tokens)
- [ ] T207 [P] Create GitHub Actions CI/CD workflow in .github/workflows/ci.yml (run linting, formatting, type checking, tests for both frontend and backend, build verification)
- [ ] T208 Create production deployment guide in DEPLOYMENT.md (environment setup, build steps, Docker deployment, environment variables, database migrations, monitoring setup)
- [ ] T209 Run load testing with 1000 concurrent users using Locust or k6 (verify API p95 <200ms/<500ms, no errors)
- [ ] T210 Run E2E regression test suite (all Playwright tests) on Chrome, Firefox, Safari, Edge latest 2 versions
- [ ] T211 Run mobile device testing on iOS Safari and Android Chrome (real devices or emulators, verify all user flows work without horizontal scroll)
- [ ] T212 Create quickstart validation script (follow quickstart.md step by step, verify all commands work, frontend and backend start successfully)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 (ProductDetail Add to Cart button) but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US2 (uses cart) but independently testable with pre-filled cart
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US3 (uses checkout data) but independently testable with pre-configured order
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Independent, optional for guest checkout flow

### Within Each User Story

- Tests (T044-T049, T071-T075, etc.) MUST be written and FAIL before implementation
- Models (T050-T051, T076-T077, etc.) before services
- Repositories (T052-T053, T078, etc.) before services
- Services (T054-T055, T079, etc.) before routes/endpoints
- API routes (T056, T080, etc.) before frontend API clients
- Frontend types and API clients (T057-T058, T081-T083, etc.) in parallel
- Frontend contexts and hooks (T084-T085, T106-T108, etc.) before components that use them
- Frontend components (T060-T065, T086-T088, etc.) in parallel (different files)
- Frontend pages (T066-T068, T089, etc.) after components they use
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T011, T013-T015, T017-T018)
- All Foundational tasks marked [P] can run in parallel (T024-T043)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each story, all tasks marked [P] can run in parallel
- All tests for a user story marked [P] can run in parallel
- All models, repositories, API clients for a story marked [P] can run in parallel
- Components within a story marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (write first, ensure they fail):
T044: "Create product service unit tests in backend/tests/unit/test_product_service.py"
T045: "Create product API integration tests in backend/tests/integration/test_products_api.py"
T046: "Create ProductCard component tests in frontend/tests/component/ProductCard.test.tsx"
T047: "Create ProductGrid component tests in frontend/tests/component/ProductGrid.test.tsx"
T048: "Create useProducts hook tests in frontend/tests/unit/useProducts.test.ts"

# Launch all models and repositories for User Story 1 together (after tests fail):
T050: "Create Product Pydantic model in backend/src/models/product.py"
T051: "Create Category Pydantic model in backend/src/models/category.py"
T052: "Create ProductRepository in backend/src/repositories/product_repository.py"
T053: "Create CategoryRepository in backend/src/repositories/category_repository.py"

# Launch all frontend components marked [P] for User Story 1 together:
T060: "Create ProductCard component in frontend/src/components/products/ProductCard.tsx"
T061: "Create ProductGrid component in frontend/src/components/products/ProductGrid.tsx"
T062: "Create SearchBar component in frontend/src/components/products/SearchBar.tsx"
T063: "Create FilterPanel component in frontend/src/components/products/FilterPanel.tsx"
T064: "Create ProductImageGallery component in frontend/src/components/products/ProductImageGallery.tsx"
T065: "Create ProductDetail component in frontend/src/components/products/ProductDetail.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T018)
2. Complete Phase 2: Foundational (T019-T043) - CRITICAL blocking phase
3. Complete Phase 3: User Story 1 (T044-T070)
4. **STOP and VALIDATE**: Test User Story 1 independently (browse products, view details)
5. Deploy/demo if ready - this is a functional product catalog

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Browse Products) → Test independently → Deploy/Demo (MVP - Product Catalog!)
3. Add User Story 2 (Shopping Cart) → Test independently → Deploy/Demo (MVP + Cart!)
4. Add User Story 3 (Checkout) → Test independently → Deploy/Demo (Almost complete purchase flow!)
5. Add User Story 4 (Payment) → Test independently → Deploy/Demo (Full e-commerce platform!)
6. Add User Story 5 (User Accounts) → Test independently → Deploy/Demo (Complete with accounts!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers (2-3 person team):

1. **Team completes Setup + Foundational together** (T001-T043)
2. **Once Foundational is done, split into parallel tracks**:
   - Developer A (Backend): User Story 1 backend (T050-T056)
   - Developer B (Frontend): User Story 1 frontend (T057-T070)
   - Developer C (Testing): User Story 1 tests (T044-T049)
3. Stories complete and integrate independently
4. Repeat pattern for User Stories 2-5

**Sprint Planning** (2-week sprints):
- **Sprint 0**: Setup + Foundational (T001-T043) - 1 week
- **Sprint 1**: User Story 1 (T044-T070) - 1-2 weeks
- **Sprint 2**: User Story 2 (T071-T093) - 1 week
- **Sprint 3**: User Story 3 (T094-T116) - 1-2 weeks
- **Sprint 4**: User Story 4 (T117-T146) - 2 weeks (payment integration is complex)
- **Sprint 5**: User Story 5 (T147-T184) - 2 weeks
- **Sprint 6**: Polish & Production Readiness (T185-T212) - 1-2 weeks

**Total**: 6-8 weeks (32-42 days) with 2-3 developers

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** maps task to specific user story for traceability (US1, US2, US3, US4, US5)
- Each user story should be **independently completable and testable**
- **Verify tests fail** before implementing (TDD approach)
- **Commit after each task** or logical group
- **Stop at any checkpoint** to validate story independently
- **Constitutional compliance**: All tasks follow clean architecture, mobile-first, accessibility, security, performance principles
- **Avoid**: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 212 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 18 tasks
- Phase 2 (Foundational): 25 tasks
- Phase 3 (US1 - Browse Products): 27 tasks (6 tests + 21 implementation)
- Phase 4 (US2 - Shopping Cart): 23 tasks (5 tests + 18 implementation)
- Phase 5 (US3 - Checkout): 23 tasks (5 tests + 18 implementation)
- Phase 6 (US4 - Payment): 30 tasks (5 tests + 25 implementation)
- Phase 7 (US5 - User Accounts): 38 tasks (6 tests + 32 implementation)
- Phase 8 (Polish): 28 tasks

**Parallel Opportunities**: ~80+ tasks marked [P] can run in parallel

**Independent Test Criteria**:
- US1: Load homepage → product listings → filters → product details
- US2: Add to cart → view cart → update quantity → remove item
- US3: Pre-filled cart → shipping info → shipping method → review order
- US4: Pre-configured order → payment info → process → confirmation
- US5: Register → login → profile → addresses → order history

**Suggested MVP Scope**: User Story 1 only (Browse Products) - 70 tasks (Setup + Foundational + US1)

---

**Tasks Status**: ✅ COMPLETE - Ready for implementation (`/sp.implement`)
