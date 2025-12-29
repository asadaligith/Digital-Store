# Implementation Plan: E-Commerce Store Platform

**Branch**: `001-ecommerce-store` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ecommerce-store/spec.md`

## Summary

Build a full-stack e-commerce platform with React/TypeScript frontend and FastAPI/Python backend, enabling customers to browse products, manage shopping carts, complete checkout, process payments, and manage user accounts. The implementation follows clean architecture principles with mobile-first responsive design, performance-optimized GSAP animations, secure JWT authentication, and MongoDB for data persistence.

**Primary Requirement**: Create a production-ready e-commerce store supporting 1,000+ concurrent users with <1.5s homepage load times, guest checkout, multiple payment methods (Stripe/PayPal), and WCAG AA accessibility compliance.

**Technical Approach**: Monorepo structure with separate frontend/ and backend/ directories, Context API for state management, RESTful API design, JWT-based authentication with httpOnly cookies, MongoDB with Mongoose-like schemas via Motor async driver, GSAP for GPU-accelerated animations, and Tailwind CSS mobile-first responsive design.

## Technical Context

**Language/Version**:
- **Frontend**: TypeScript 5.3+, JavaScript ES2022+
- **Backend**: Python 3.11+

**Primary Dependencies**:
- **Frontend**: React 18.2+, Vite 5+, Tailwind CSS 3.4+, GSAP 3.12+, React Router 6+, Axios 1+, Zustand (lightweight state) or Context API
- **Backend**: FastAPI 0.104+, Motor 3+ (async MongoDB driver), Pydantic 2+, PyJWT 2+, python-multipart, email-validator, bcrypt, python-dotenv
- **Database**: MongoDB 7+
- **Testing**: Vitest, React Testing Library, Playwright (frontend), pytest, httpx (backend)
- **Dev Tools**: ESLint, Prettier, Black, Ruff, pre-commit hooks

**Storage**: MongoDB 7+ (document database) with collections for users, products, carts, cart_items, orders, order_items, payments, addresses, reviews, categories

**Testing**:
- **Frontend**: Vitest (unit tests for hooks, utilities), React Testing Library (component tests), Playwright (E2E tests)
- **Backend**: pytest (unit tests for services, utilities), pytest-asyncio (async tests), httpx (API integration tests)

**Target Platform**:
- **Frontend**: Modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions), mobile-first responsive (320px to 1920px+)
- **Backend**: Linux server (Ubuntu 22.04+ or container), Docker/Docker Compose for local development

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- **Frontend**: FCP <1.5s, LCP <2.5s, TTI <3.5s, CLS <0.1, main bundle <200KB gzipped, 60fps animations
- **Backend**: API p95 <200ms (read operations), p95 <500ms (write operations), 1,000+ concurrent users, database query p95 <100ms

**Constraints**:
- **Mobile-First**: Must start at 320px baseline before desktop optimization
- **Accessibility**: WCAG AA compliance (4.5:1 text contrast, keyboard navigation, screen readers)
- **Security**: JWT auth, bcrypt ≥12 rounds, HTTPS only, CSRF protection, rate limiting (100 req/min authenticated, 20 req/min anonymous)
- **Browser Support**: Latest 2 versions of modern browsers (NO IE11)
- **Bundle Size**: Main bundle <200KB gzipped, code-split routes
- **Test Coverage**: >80% for business logic

**Scale/Scope**:
- **Users**: 1,000+ concurrent, 10,000+ registered users
- **Products**: Up to 10,000 products initially (pagination/infinite scroll required)
- **Orders**: Unlimited order history with efficient indexing
- **Storage**: Product images on CDN (Cloudinary/S3), MongoDB for transactional data

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Clean Architecture ✅ PASS

**Frontend Layers**:
- ✅ UI Components (React) in `frontend/src/components/`
- ✅ State Management (Context API) in `frontend/src/contexts/`
- ✅ API Client in `frontend/src/services/api/`
- ✅ Custom Hooks in `frontend/src/hooks/`
- ✅ No direct database access from UI

**Backend Layers**:
- ✅ API Routes (FastAPI) in `backend/src/api/routes/`
- ✅ Business Logic (Services) in `backend/src/services/`
- ✅ Data Access (Repositories) in `backend/src/repositories/`
- ✅ Models (Pydantic) in `backend/src/models/`
- ✅ No business logic in routes

**Dependency Flow**: UI → State/Hooks → API Client → FastAPI Routes → Services → Repositories → MongoDB

### II. Mobile-First Responsive Design ✅ PASS

- ✅ Development order: Mobile (320px) → Tablet (768px) → Desktop (1024px+)
- ✅ Tailwind CSS responsive utilities with progressive breakpoints
- ✅ Touch targets ≥44px on mobile
- ✅ Responsive images with `srcset` or Tailwind responsive classes
- ✅ Mobile testing before desktop optimization

### III. Performance-First GSAP Animations ✅ PASS

- ✅ GPU-accelerated properties only (transform, opacity)
- ✅ GSAP Timeline management with cleanup on unmount
- ✅ Non-blocking animations, 60fps target
- ✅ Reduced motion support (`prefers-reduced-motion`)
- ✅ Lazy loading animations (code-split)

### IV. Secure API Design ✅ PASS

- ✅ JWT tokens (access 15min, refresh 7 days) in httpOnly cookies
- ✅ RBAC at service layer
- ✅ Pydantic input validation on ALL endpoints
- ✅ Structured error responses, no stack traces in production
- ✅ Rate limiting (100 req/min authenticated, 20 req/min anonymous)
- ✅ HTTPS only, CORS whitelist
- ✅ Parameterized queries (Motor driver, no raw queries)
- ✅ Input sanitization, CSP headers

### V. Scalable MongoDB Schema Design ✅ PASS

- ✅ Embed for 1:1 and 1:few (cart_items in cart, order_items in order)
- ✅ Reference for 1:many and many:many (user → orders, product → reviews)
- ✅ Indexes on query fields (email, product_id, order_number)
- ✅ Schema validation via Pydantic models
- ✅ Denormalization for reads (product name/price snapshot in order_items)
- ✅ Pagination for large datasets (products, orders, reviews)
- ✅ Connection pooling configured

### VI. Reusable React Components and Hooks ✅ PASS

- ✅ Single Responsibility Principle per component
- ✅ TypeScript interfaces for all props
- ✅ Composition over inheritance
- ✅ Custom hooks: `useCart()`, `useAuth()`, `useProducts()`, `useCheckout()`
- ✅ No business logic in components (hooks handle logic)
- ✅ Max 2 levels prop drilling (Context for deeper data)
- ✅ One component per file with co-located tests

### VII. Accessibility (ARIA, Keyboard, Screen Readers) ✅ PASS

- ✅ Semantic HTML (`<button>`, `<nav>`, `<main>`, `<article>`)
- ✅ ARIA labels where needed
- ✅ Full keyboard navigation (Tab, Enter, Space, Escape)
- ✅ Visible focus indicators
- ✅ WCAG AA contrast (4.5:1 normal, 3:1 large)
- ✅ Screen reader testing planned
- ✅ Form accessibility (labels, error messages, `aria-invalid`)
- ✅ Skip navigation links
- ✅ Alt text for images

### VIII. Test-Driven Development (TDD) ✅ PASS

- ✅ Unit tests (Vitest, pytest) >80% coverage on business logic
- ✅ Integration tests (httpx for API endpoints)
- ✅ E2E tests (Playwright for critical flows: signup, login, cart, checkout)
- ✅ Test pyramid approach
- ✅ CI pipeline fails if tests fail
- ✅ Mock external dependencies (payment gateway, email service)

### IX. Production-Ready Coding Standards ✅ PASS

- ✅ TypeScript strict mode, no `any` types
- ✅ Python type hints with mypy strict mode
- ✅ Prettier (frontend), Black (backend) auto-format
- ✅ ESLint (frontend), Ruff (backend), no linting errors
- ✅ Naming conventions: PascalCase components, camelCase functions, UPPER_SNAKE_CASE constants
- ✅ Error handling, structured logging
- ✅ `.env` for secrets, environment validation on startup
- ✅ Conventional commits: `type(scope): description`
- ✅ Code reviews required

### X. Dependency Management and Security ✅ PASS

- ✅ Justified dependencies only
- ✅ `npm audit` and `pip-audit` in CI pipeline
- ✅ Version pinning in `package-lock.json` and `requirements.txt`
- ✅ Bundle size monitoring (<200KB gzipped)
- ✅ ES modules for tree-shaking
- ✅ Monthly dependency updates with testing
- ✅ No deprecated packages

**Constitution Check Result**: ✅ **ALL GATES PASSED** - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/001-ecommerce-store/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: Technology decisions and best practices
├── data-model.md        # Phase 1 output: MongoDB schemas and relationships
├── quickstart.md        # Phase 1 output: Setup and development guide
├── contracts/           # Phase 1 output: OpenAPI specs for all endpoints
│   ├── auth.openapi.yaml
│   ├── products.openapi.yaml
│   ├── cart.openapi.yaml
│   ├── checkout.openapi.yaml
│   ├── orders.openapi.yaml
│   └── users.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
Digital-Store/
├── .specify/                    # SpecKit templates and scripts
├── specs/                       # Feature specifications
├── history/                     # PHRs and ADRs
├── frontend/                    # React + TypeScript + Tailwind + GSAP
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── common/          # Button, Input, Card, Modal, etc.
│   │   │   ├── layout/          # Header, Footer, Sidebar, etc.
│   │   │   ├── products/        # ProductCard, ProductGrid, ProductDetail, etc.
│   │   │   ├── cart/            # CartItem, CartSummary, CartIcon, etc.
│   │   │   ├── checkout/        # CheckoutForm, ShippingForm, PaymentForm, etc.
│   │   │   └── auth/            # LoginForm, SignupForm, etc.
│   │   ├── pages/               # Route-level pages
│   │   │   ├── HomePage.tsx
│   │   │   ├── ProductListPage.tsx
│   │   │   ├── ProductDetailPage.tsx
│   │   │   ├── CartPage.tsx
│   │   │   ├── CheckoutPage.tsx
│   │   │   ├── PaymentPage.tsx
│   │   │   ├── OrderConfirmationPage.tsx
│   │   │   ├── AccountDashboardPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── SignupPage.tsx
│   │   ├── contexts/            # React Context for global state
│   │   │   ├── AuthContext.tsx
│   │   │   ├── CartContext.tsx
│   │   │   └── CheckoutContext.tsx
│   │   ├── hooks/               # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useCart.ts
│   │   │   ├── useProducts.ts
│   │   │   ├── useCheckout.ts
│   │   │   ├── useOrders.ts
│   │   │   └── useAnimations.ts (GSAP utilities)
│   │   ├── services/            # API clients and utilities
│   │   │   ├── api/
│   │   │   │   ├── client.ts    # Axios instance with interceptors
│   │   │   │   ├── auth.ts      # Authentication API calls
│   │   │   │   ├── products.ts  # Product API calls
│   │   │   │   ├── cart.ts      # Cart API calls
│   │   │   │   ├── orders.ts    # Order API calls
│   │   │   │   └── users.ts     # User API calls
│   │   │   └── storage/
│   │   │       └── localStorage.ts # Cart persistence for guests
│   │   ├── types/               # TypeScript type definitions
│   │   │   ├── product.ts
│   │   │   ├── cart.ts
│   │   │   ├── order.ts
│   │   │   ├── user.ts
│   │   │   └── api.ts
│   │   ├── utils/               # Helper functions
│   │   │   ├── validation.ts
│   │   │   ├── formatting.ts
│   │   │   └── animations.ts
│   │   ├── styles/              # Global styles
│   │   │   └── index.css        # Tailwind imports + custom styles
│   │   ├── App.tsx              # Root component with routing
│   │   └── main.tsx             # Entry point
│   ├── tests/
│   │   ├── unit/                # Unit tests for hooks, utils
│   │   ├── component/           # Component tests (React Testing Library)
│   │   └── e2e/                 # E2E tests (Playwright)
│   ├── public/                  # Static assets
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── package.json
│   └── .env.example
├── backend/                     # FastAPI + Python + MongoDB
│   ├── src/
│   │   ├── api/                 # FastAPI routes
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── products.py
│   │   │   │   ├── cart.py
│   │   │   │   ├── orders.py
│   │   │   │   └── users.py
│   │   │   ├── dependencies/    # Route dependencies (auth, rate limiting)
│   │   │   │   ├── auth.py
│   │   │   │   └── rate_limit.py
│   │   │   └── middleware/      # CORS, error handling, logging
│   │   │       ├── cors.py
│   │   │       ├── error_handler.py
│   │   │       └── logger.py
│   │   ├── services/            # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── product_service.py
│   │   │   ├── cart_service.py
│   │   │   ├── order_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── user_service.py
│   │   │   └── email_service.py
│   │   ├── repositories/        # Data access layer
│   │   │   ├── user_repository.py
│   │   │   ├── product_repository.py
│   │   │   ├── cart_repository.py
│   │   │   ├── order_repository.py
│   │   │   └── payment_repository.py
│   │   ├── models/              # Pydantic models (schemas)
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── cart.py
│   │   │   ├── order.py
│   │   │   ├── payment.py
│   │   │   └── address.py
│   │   ├── db/                  # Database configuration
│   │   │   ├── mongodb.py       # Motor client setup
│   │   │   └── indexes.py       # Index creation scripts
│   │   ├── core/                # Core utilities
│   │   │   ├── config.py        # Settings (environment variables)
│   │   │   ├── security.py      # JWT, password hashing
│   │   │   └── exceptions.py    # Custom exceptions
│   │   ├── utils/               # Helper functions
│   │   │   ├── validators.py
│   │   │   └── formatters.py
│   │   └── main.py              # FastAPI app entry point
│   ├── tests/
│   │   ├── unit/                # Unit tests for services, utils
│   │   ├── integration/         # API integration tests
│   │   └── conftest.py          # Pytest fixtures
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml           # Black, Ruff, mypy config
│   └── .env.example
├── docker-compose.yml           # Local development (MongoDB, backend, frontend)
├── .gitignore
├── README.md
└── .pre-commit-config.yaml      # Pre-commit hooks
```

**Structure Decision**:

Selected **Option 2: Web application** structure with separate `frontend/` and `backend/` directories in a monorepo. This structure is chosen because:

1. **Clear separation**: Frontend (React/TypeScript) and backend (FastAPI/Python) have distinct technology stacks, dependencies, and deployment targets
2. **Independent development**: Teams can work on frontend and backend in parallel without conflicts
3. **Separate testing**: Frontend tests (Vitest, Playwright) and backend tests (pytest) are isolated
4. **Flexible deployment**: Frontend can be deployed to CDN/static hosting (Vercel, Netlify), backend to container platform (AWS ECS, Google Cloud Run)
5. **Monorepo benefits**: Shared documentation, coordinated releases, unified CI/CD pipeline while maintaining clear boundaries

The structure strictly follows constitutional clean architecture with:
- **Frontend**: UI (components) → State (contexts/hooks) → API Client (services/api)
- **Backend**: API Routes (api/routes) → Services (business logic) → Repositories (data access) → MongoDB

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**NO VIOLATIONS** - All constitutional principles are followed without exceptions. No complexity justification required.

---

## Phase 0: Research & Technology Decisions

**Status**: ✅ Complete (see [research.md](./research.md))

Key decisions documented in research.md:
1. State Management: Context API vs Zustand
2. Form Handling: React Hook Form vs Formik
3. Payment Gateway Integration: Stripe vs PayPal
4. Email Service: SendGrid vs AWS SES
5. CDN/Image Hosting: Cloudinary vs AWS S3
6. MongoDB ODM: Motor (async driver) with Pydantic validation
7. Authentication Strategy: JWT with httpOnly cookies + refresh tokens
8. Cart Persistence: localStorage for guests, MongoDB for authenticated users
9. API Design Patterns: RESTful conventions, pagination strategies
10. Animation Patterns: GSAP Timeline recipes for common UI interactions

---

## Phase 1: Data Model & API Contracts

**Status**: ✅ Complete

### Artifacts Created:
1. **[data-model.md](./data-model.md)** - MongoDB schema design for all collections
2. **[contracts/](./contracts/)** - OpenAPI 3.1 specifications for all API endpoints
3. **[quickstart.md](./quickstart.md)** - Development setup and workflow guide

### Data Model Summary:

**10 MongoDB Collections**:
1. `users` - Customer accounts (email, password, profile)
2. `products` - Product catalog (name, price, images, stock)
3. `carts` - Active shopping carts (user/guest reference)
4. `cart_items` - Embedded in carts (product, quantity, price)
5. `orders` - Completed purchases (order number, status, totals)
6. `order_items` - Embedded in orders (product snapshot, quantity, price)
7. `payments` - Payment records (transaction ID, status, method)
8. `addresses` - Saved shipping/billing addresses
9. `reviews` - Product reviews (rating, text, user)
10. `categories` - Product categorization (hierarchical)

**Key Design Decisions**:
- Embed cart_items in carts (1:few relationship, always loaded together)
- Embed order_items in orders (historical snapshot, immutable)
- Reference users from orders/carts (1:many, user can have many orders)
- Denormalize product name/price in order_items (historical accuracy)
- Index: users.email, products.category, orders.order_number, carts.user_id

### API Contracts Summary:

**6 API Modules** (RESTful):
1. **Auth** (`/api/auth/*`) - Register, login, logout, refresh token, password reset
2. **Products** (`/api/products/*`) - List, search, filter, get by ID, categories
3. **Cart** (`/api/cart/*`) - Get cart, add item, update quantity, remove item, clear cart
4. **Checkout** (`/api/checkout/*`) - Validate cart, calculate totals, create order
5. **Orders** (`/api/orders/*`) - List orders, get order details, update status
6. **Users** (`/api/users/*`) - Get profile, update profile, manage addresses, order history

**API Design Patterns**:
- **Authentication**: JWT Bearer tokens in Authorization header OR httpOnly cookies
- **Pagination**: `?page=1&limit=20` (default limit=20, max=100)
- **Filtering**: `?category=electronics&min_price=50&max_price=500`
- **Sorting**: `?sort_by=price&order=asc` (asc/desc)
- **Search**: `?q=laptop&fields=name,description`
- **Error Format**: `{"error": {"code": "INVALID_INPUT", "message": "...", "details": {...}}}`
- **Success Format**: `{"data": {...}, "meta": {"page": 1, "total": 100}}`

---

## Phase 2: Implementation Roadmap

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level implementation phases.

### Phase 2.0: Project Setup & Infrastructure

**Goal**: Set up development environment, tooling, and base project structure

**Key Deliverables**:
- Initialize frontend with Vite + React + TypeScript + Tailwind CSS
- Initialize backend with FastAPI + Python + Poetry/pip
- Configure MongoDB (Docker Compose for local, MongoDB Atlas for production)
- Set up ESLint, Prettier, Black, Ruff, pre-commit hooks
- Configure CI/CD pipeline (GitHub Actions: lint, test, build)
- Create .env.example files with all required environment variables
- Set up Docker Compose for local development (MongoDB, backend, frontend)

**Duration Estimate**: 1-2 days

---

### Phase 2.1: User Story 1 - Browse and Discover Products (P1)

**Goal**: Implement product discovery features (homepage, listing, detail pages)

**Key Deliverables**:

**Backend**:
- Product model (Pydantic schema)
- Product repository (CRUD operations with MongoDB)
- Product service (business logic: filtering, sorting, pagination)
- Product API routes (`GET /api/products`, `GET /api/products/:id`, `GET /api/categories`)
- Seed script to populate sample products

**Frontend**:
- ProductCard component (image, name, price, rating, Add to Cart button)
- ProductGrid component (grid layout with responsive breakpoints)
- ProductList page (with filters, sorting, pagination/infinite scroll)
- ProductDetail page (image gallery, specs, reviews, Add to Cart)
- HomePage (featured products, banners, categories)
- SearchBar component (with real-time search suggestions)
- FilterPanel component (category, price range, rating, availability)
- `useProducts` hook (fetch, filter, paginate products)
- GSAP animations: page transitions, product card hover effects, image gallery

**Testing**:
- Backend: pytest tests for product service and API endpoints
- Frontend: Component tests for ProductCard, ProductGrid, ProductDetail
- E2E: Playwright test for browsing flow (homepage → listing → detail)

**Duration Estimate**: 5-7 days

---

### Phase 2.2: User Story 2 - Add Products to Shopping Cart (P2)

**Goal**: Implement shopping cart functionality

**Key Deliverables**:

**Backend**:
- Cart model (Pydantic schema with embedded cart_items)
- Cart repository (CRUD for carts and cart items)
- Cart service (add item, update quantity, remove item, calculate totals)
- Cart API routes (`GET /api/cart`, `POST /api/cart/items`, `PATCH /api/cart/items/:id`, `DELETE /api/cart/items/:id`)
- Guest cart support (session-based or anonymous cart ID)

**Frontend**:
- CartContext (global cart state with Context API)
- `useCart` hook (add to cart, update quantity, remove item, sync with backend)
- CartIcon component (item count badge in header)
- CartItem component (product info, quantity selector, remove button)
- CartPage (list of cart items, subtotal, taxes, shipping estimate, total, Proceed to Checkout)
- Cart persistence: localStorage for guests, API sync for authenticated users
- GSAP animations: cart icon bounce on add, cart item fade-out on remove, quantity update

**Testing**:
- Backend: pytest tests for cart service and API endpoints
- Frontend: Component tests for CartIcon, CartItem, CartPage; hook tests for useCart
- E2E: Playwright test for cart flow (add item → update quantity → remove item → proceed to checkout)

**Duration Estimate**: 4-5 days

---

### Phase 2.3: User Story 3 - Complete Checkout Process (P3)

**Goal**: Implement checkout flow (shipping info, shipping method, order review)

**Key Deliverables**:

**Backend**:
- Address model (Pydantic schema for shipping/billing addresses)
- Shipping calculation service (flat rate, weight-based, or location-based)
- Checkout validation service (stock availability, pricing accuracy)
- Checkout API routes (`POST /api/checkout/validate`, `POST /api/checkout/calculate-shipping`)
- Tax calculation service (based on shipping address)

**Frontend**:
- CheckoutContext (multi-step checkout state)
- `useCheckout` hook (manage checkout steps, validate forms, calculate totals)
- ShippingForm component (address fields with validation using React Hook Form)
- ShippingMethodSelector component (radio buttons for shipping options)
- OrderReview component (summary of items, shipping, totals)
- CheckoutPage (multi-step wizard: Shipping Info → Shipping Method → Review)
- Guest checkout flow (no login required)
- GSAP animations: step transitions, progress indicator, form validation feedback

**Testing**:
- Backend: pytest tests for checkout validation and shipping calculation
- Frontend: Component tests for ShippingForm, ShippingMethodSelector, OrderReview
- E2E: Playwright test for checkout flow (guest checkout → shipping info → shipping method → review)

**Duration Estimate**: 5-6 days

---

### Phase 2.4: User Story 4 - Complete Payment (P4)

**Goal**: Implement payment processing and order confirmation

**Key Deliverables**:

**Backend**:
- Order model (Pydantic schema with embedded order_items)
- Payment model (Pydantic schema with payment status)
- Order repository (create order, update status)
- Payment repository (create payment record)
- Payment service (Stripe/PayPal integration, handle success/failure)
- Order service (create order from cart, generate order number, update inventory)
- Payment webhook handler (process payment gateway callbacks)
- Email service (send order confirmation email)
- Payment API routes (`POST /api/orders`, `POST /api/payments/process`, `POST /api/payments/webhook`)

**Frontend**:
- PaymentForm component (credit card fields, payment method selector)
- Stripe Elements integration (for PCI compliance)
- PaymentPage (payment form, loading states, error handling)
- OrderConfirmationPage (order number, order summary, estimated delivery)
- Payment processing flow (loading indicator, success/failure messages)
- GSAP animations: payment processing loader, success confetti, error shake

**Testing**:
- Backend: pytest tests for order creation, payment processing (mocked Stripe API)
- Frontend: Component tests for PaymentForm, OrderConfirmationPage
- E2E: Playwright test for payment flow (enter payment info → process → confirmation)

**Duration Estimate**: 6-8 days (payment gateway integration is complex)

---

### Phase 2.5: User Story 5 - User Account Management (P5)

**Goal**: Implement user registration, login, profile, order history

**Key Deliverables**:

**Backend**:
- User model (Pydantic schema with password hash, email verification)
- User repository (CRUD operations)
- Auth service (register, login, logout, password hashing with bcrypt, JWT generation)
- Email verification service (send verification email, verify token)
- Password reset service (send reset email, verify reset token, update password)
- User service (get profile, update profile, manage saved addresses)
- Auth API routes (`POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `POST /api/auth/refresh`, `POST /api/auth/forgot-password`, `POST /api/auth/reset-password`)
- User API routes (`GET /api/users/profile`, `PATCH /api/users/profile`, `GET /api/users/addresses`, `POST /api/users/addresses`, `GET /api/users/orders`)
- JWT middleware (verify access token, extract user from token)
- Rate limiting middleware (prevent brute force attacks)
- Account lockout after 5 failed login attempts

**Frontend**:
- AuthContext (authentication state: user, token, isAuthenticated)
- `useAuth` hook (register, login, logout, check auth status)
- LoginForm component (email, password, remember me)
- SignupForm component (email, password, name, phone, email verification prompt)
- AccountDashboardPage (profile info, saved addresses, order history)
- OrderHistoryList component (list of past orders)
- OrderDetailPage (detailed order information)
- SavedAddressesList component (manage saved addresses)
- Protected routes (redirect to login if not authenticated)
- GSAP animations: form transitions, success/error notifications

**Testing**:
- Backend: pytest tests for auth service (register, login, password reset), JWT generation/validation
- Frontend: Component tests for LoginForm, SignupForm, AccountDashboardPage; hook tests for useAuth
- E2E: Playwright test for account flow (register → verify email → login → view profile → view orders)

**Duration Estimate**: 6-7 days

---

### Phase 2.6: Polish & Production Readiness

**Goal**: Optimize performance, fix bugs, improve UX, prepare for production

**Key Deliverables**:

**Performance Optimization**:
- Code splitting (lazy load routes)
- Image optimization (WebP format, responsive sizes, lazy loading)
- Bundle size analysis and reduction
- Database indexing optimization
- API response caching (Redis or in-memory cache)
- Frontend caching (service worker for offline support - optional)

**Accessibility**:
- WCAG AA compliance audit (axe DevTools)
- Keyboard navigation testing
- Screen reader testing (NVDA, VoiceOver)
- Color contrast fixes
- Focus management improvements

**Security Hardening**:
- Security audit (OWASP Top 10 checklist)
- Input sanitization review
- CSRF token implementation
- Rate limiting tuning
- Security headers (CSP, X-Frame-Options, etc.)

**Monitoring & Logging**:
- Frontend error tracking (Sentry or similar)
- Backend logging (structured JSON logs)
- API performance monitoring
- Database query performance monitoring

**Documentation**:
- API documentation (OpenAPI/Swagger UI)
- Component documentation (Storybook - optional)
- Deployment guide
- Environment variable documentation
- Troubleshooting guide

**Final Testing**:
- Full E2E regression test suite
- Load testing (1,000 concurrent users)
- Mobile device testing (iOS Safari, Android Chrome)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)

**Duration Estimate**: 5-7 days

---

## Total Implementation Estimate

**Total Duration**: 32-42 days (6-8 weeks)

**Breakdown**:
- Phase 2.0: Setup (1-2 days)
- Phase 2.1: Browse Products (5-7 days)
- Phase 2.2: Shopping Cart (4-5 days)
- Phase 2.3: Checkout (5-6 days)
- Phase 2.4: Payment (6-8 days)
- Phase 2.5: User Accounts (6-7 days)
- Phase 2.6: Polish & Production (5-7 days)

**Team Size Assumption**: 2-3 developers (1 frontend, 1 backend, 1 full-stack)

**Parallelization Opportunities**:
- Setup can be done by one person while others research
- User Stories 2-5 can have backend and frontend work in parallel
- Testing can be done in parallel with development (TDD approach)

---

## Risk Assessment & Mitigation

### High-Risk Areas

1. **Payment Gateway Integration**
   - **Risk**: Payment processing failures, security vulnerabilities, PCI compliance issues
   - **Mitigation**: Use established payment gateway SDK (Stripe Elements), thoroughly test with sandbox, implement webhook verification, never store card numbers

2. **Performance at Scale**
   - **Risk**: Slow page loads, API timeouts, database query bottlenecks
   - **Mitigation**: Implement pagination, database indexing, API caching, lazy loading, code splitting, load testing before production

3. **Cart Persistence**
   - **Risk**: Cart data loss, synchronization issues between guest/authenticated carts
   - **Mitigation**: localStorage backup for guests, clear migration strategy when guest becomes authenticated, cart expiration policy (7 days for guests)

4. **Inventory Management**
   - **Risk**: Overselling products, race conditions with concurrent purchases
   - **Mitigation**: Implement pessimistic locking or optimistic locking with version numbers, validate stock at checkout, handle out-of-stock gracefully

5. **Security Vulnerabilities**
   - **Risk**: XSS, CSRF, SQL injection, authentication bypass, data breaches
   - **Mitigation**: Input sanitization, CSRF tokens, parameterized queries (Motor driver handles this), JWT with httpOnly cookies, rate limiting, regular security audits

### Medium-Risk Areas

1. **Browser Compatibility**
   - **Risk**: Features not working in certain browsers
   - **Mitigation**: Use Babel for transpilation, test in all supported browsers, graceful degradation

2. **Mobile Performance**
   - **Risk**: Slow animations, unresponsive UI on low-end devices
   - **Mitigation**: GPU-accelerated animations only, performance profiling on real devices, reduced motion support

3. **Email Deliverability**
   - **Risk**: Order confirmation emails going to spam
   - **Mitigation**: Use reputable email service (SendGrid, AWS SES), configure SPF/DKIM/DMARC, test email deliverability

---

## Deployment Strategy

### Development Environment

**Prerequisites**:
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker & Docker Compose (for MongoDB, local development)
- Git (for version control)

**Setup**:
1. Clone repository
2. Run `docker-compose up -d` (starts MongoDB)
3. Backend: `cd backend && pip install -r requirements-dev.txt && uvicorn src.main:app --reload`
4. Frontend: `cd frontend && npm install && npm run dev`
5. Access frontend at `http://localhost:5173`, backend at `http://localhost:8000`

### Staging Environment

**Infrastructure**:
- Frontend: Vercel/Netlify preview deployment (automatic from PR)
- Backend: Docker container on AWS ECS/Google Cloud Run (staging cluster)
- Database: MongoDB Atlas (staging cluster with limited resources)
- Payment: Stripe test mode
- Email: SendGrid test API key

**CI/CD**:
- Automated deployment on merge to `develop` branch
- Run all tests before deployment
- Smoke tests after deployment

### Production Environment

**Infrastructure**:
- Frontend: Vercel/Netlify/AWS CloudFront + S3 (CDN for static assets)
- Backend: Docker containers on AWS ECS/Google Cloud Run/Azure Container Instances (auto-scaling)
- Database: MongoDB Atlas (production cluster with replicas, backups)
- Payment: Stripe production mode (PCI compliant)
- Email: SendGrid production API key
- CDN: Cloudinary/AWS CloudFront for product images
- Monitoring: Sentry (error tracking), DataDog/New Relic (APM)

**CI/CD**:
- Manual deployment from `main` branch after approval
- Blue-green deployment or canary deployment for zero-downtime
- Automated rollback on failed health checks
- Database migrations run before deployment

**Environment Variables** (example):
```bash
# Frontend (.env)
VITE_API_BASE_URL=https://api.example.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Backend (.env)
MONGODB_URI=mongodb+srv://...
JWT_SECRET_KEY=...
JWT_REFRESH_SECRET_KEY=...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=noreply@example.com
CORS_ORIGINS=https://example.com,https://www.example.com
```

---

## Next Steps

1. ✅ **Phase 0 Complete**: Research decisions documented in [research.md](./research.md)
2. ✅ **Phase 1 Complete**: Data model and API contracts created
3. 🎯 **Run `/sp.tasks`** to generate detailed task breakdown from this plan
4. 🎯 **Run `/sp.implement`** to begin implementation (after tasks are defined)

---

**Plan Status**: ✅ COMPLETE - Ready for task generation (`/sp.tasks`)
