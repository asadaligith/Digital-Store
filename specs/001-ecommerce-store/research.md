# Technology Research & Decisions: E-Commerce Store Platform

**Feature**: E-Commerce Store Platform
**Branch**: `001-ecommerce-store`
**Date**: 2025-12-29
**Phase**: Phase 0 - Research & Technology Selection

## Overview

This document consolidates all technology research and architectural decisions for the E-Commerce Store implementation. Each decision is documented with rationale, alternatives considered, and best practices.

---

## 1. State Management: Context API vs Zustand

### Decision: **Context API** (with potential Zustand for complex cart state)

### Rationale:
- **Context API**: Built into React, zero dependencies, sufficient for auth state and simple global state
- **Zustand**: Lightweight (1KB), better performance for frequent updates (cart operations), simpler API than Redux
- **Hybrid Approach**: Use Context API for auth/checkout, consider Zustand for cart if performance issues arise

### Alternatives Considered:
1. **Redux Toolkit** - Rejected: Too heavy for this use case (adds ~50KB), boilerplate overhead, overkill for 3 contexts
2. **Recoil** - Rejected: Still experimental, smaller ecosystem, unnecessary complexity
3. **Jotai** - Rejected: Atomic state model is overkill for our simple global state needs

### Best Practices:
- Separate contexts by domain (AuthContext, CartContext, CheckoutContext)
- Use `useReducer` for complex state logic (cart calculations, checkout wizard)
- Memoize context values with `useMemo` to prevent unnecessary re-renders
- Split context providers to avoid re-rendering entire app on any state change
- Consider Zustand if cart operations become performance bottleneck (>50ms updates)

### Implementation Notes:
```typescript
// AuthContext: User authentication state
// CartContext: Shopping cart state with localStorage sync
// CheckoutContext: Multi-step checkout wizard state
```

---

## 2. Form Handling: React Hook Form vs Formik

### Decision: **React Hook Form**

### Rationale:
- **Performance**: Uncontrolled components, fewer re-renders (30-50% faster than Formik)
- **Bundle Size**: 8KB (vs Formik 15KB + Yup 20KB = 35KB)
- **TypeScript Support**: First-class TypeScript support with typed form values
- **Validation**: Native integration with Yup, Zod, or custom validators
- **DevTools**: React Hook Form DevTools for debugging

### Alternatives Considered:
1. **Formik** - Rejected: Heavier bundle, more re-renders, requires Yup for validation
2. **Final Form** - Rejected: Less popular, smaller ecosystem, documentation gaps
3. **Controlled Forms (useState)** - Rejected: Manual validation, no built-in error handling, verbose

### Best Practices:
- Use `react-hook-form` with Zod for type-safe validation schemas
- Implement field-level validation for immediate feedback
- Use `Controller` component for third-party UI libraries (e.g., date pickers)
- Extract reusable form schemas (e.g., addressSchema, paymentSchema)
- Implement async validation for email uniqueness check

### Implementation Notes:
```typescript
// Shipping form: useForm + Zod validation
// Payment form: useForm + Stripe Elements integration
// Login/Signup: useForm with async validation (email check)
```

---

## 3. Payment Gateway Integration: Stripe vs PayPal

### Decision: **Stripe** (primary), with PayPal as secondary option

### Rationale:
- **Stripe**:
  - Superior developer experience (Stripe Elements, Stripe.js)
  - PCI compliance handled by Stripe (never touch card numbers)
  - Better documentation, webhooks, and testing tools
  - Lower transaction fees (2.9% + $0.30 vs PayPal 3.49% + $0.49 for guest checkout)
  - Modern API with TypeScript support
- **PayPal**: Optional secondary payment method for users who prefer PayPal

### Alternatives Considered:
1. **PayPal Only** - Rejected: Higher fees, less developer-friendly API, limited customization
2. **Square** - Rejected: Primarily for in-person payments, limited e-commerce features
3. **Braintree** (owned by PayPal) - Rejected: More complex than Stripe, similar fees

### Best Practices:
- **Stripe Elements**: Use pre-built UI components for PCI compliance
- **Webhooks**: Implement webhook handlers for asynchronous payment confirmation
- **Idempotency**: Use idempotency keys to prevent duplicate charges on retry
- **3D Secure**: Enable SCA (Strong Customer Authentication) for European customers
- **Test Mode**: Use Stripe test mode with test card numbers (4242 4242 4242 4242)
- **Error Handling**: Map Stripe error codes to user-friendly messages

### Implementation Notes:
```typescript
// Frontend: @stripe/stripe-js + @stripe/react-stripe-js
// Backend: stripe Python SDK
// Webhook endpoint: /api/payments/webhook (verify signature)
```

### Stripe Integration Checklist:
- [ ] Create Stripe account and get API keys
- [ ] Install Stripe SDK (frontend + backend)
- [ ] Implement Stripe Elements for card input
- [ ] Create PaymentIntent on backend
- [ ] Confirm payment on frontend
- [ ] Set up webhook endpoint for payment confirmation
- [ ] Handle 3D Secure authentication flow
- [ ] Test with Stripe test cards

---

## 4. Email Service: SendGrid vs AWS SES

### Decision: **SendGrid**

### Rationale:
- **SendGrid**:
  - Easier setup (no AWS account complexity)
  - Free tier: 100 emails/day (sufficient for MVP)
  - Better deliverability (warm-up IPs, reputation monitoring)
  - Email templates with dynamic content
  - Click/open tracking, bounce handling
  - Better documentation and Python SDK
- **AWS SES**: Cheaper at scale (large volumes), but requires AWS expertise

### Alternatives Considered:
1. **AWS SES** - Deferred to later: Better for high volume (>10k emails/month), requires AWS account, more setup complexity
2. **Mailgun** - Rejected: Similar to SendGrid but less generous free tier (5k emails total, not monthly)
3. **Postmark** - Rejected: Transactional email only, no free tier, $15/month minimum
4. **Gmail SMTP** - Rejected: Daily send limits (500), poor deliverability, unprofessional

### Best Practices:
- **SPF/DKIM/DMARC**: Configure DNS records for email authentication
- **Templates**: Use SendGrid dynamic templates (avoid inline HTML in code)
- **Categories**: Tag emails by type (order_confirmation, password_reset, verification)
- **Unsubscribe Link**: Include unsubscribe link in marketing emails (GDPR compliance)
- **Rate Limiting**: Respect SendGrid's rate limits (600 emails/minute)
- **Error Handling**: Retry failed sends with exponential backoff

### Implementation Notes:
```python
# Backend: sendgrid Python SDK
# Email types: order confirmation, email verification, password reset
# Template IDs stored in environment variables
```

### Email Templates Required:
1. **Order Confirmation** - Order number, items, total, shipping address
2. **Email Verification** - Verification link with token (1hr expiry)
3. **Password Reset** - Reset link with token (1hr expiry)
4. **Shipping Notification** - Order shipped, tracking number (future iteration)

---

## 5. CDN/Image Hosting: Cloudinary vs AWS S3

### Decision: **Cloudinary**

### Rationale:
- **Cloudinary**:
  - Free tier: 25GB storage, 25GB bandwidth/month (sufficient for MVP)
  - Automatic image optimization (format conversion, quality, lazy loading)
  - On-the-fly transformations (resize, crop, format) via URL parameters
  - CDN included (no separate setup)
  - Better DX (simpler API than S3 + CloudFront)
  - Upload widget for easy image uploads
- **AWS S3**: Cheaper at massive scale, but requires CloudFront setup for CDN

### Alternatives Considered:
1. **AWS S3 + CloudFront** - Deferred to later: Better for massive scale (>100GB), more complex setup, requires AWS expertise
2. **Imgix** - Rejected: More expensive ($10/month minimum), similar features to Cloudinary
3. **Local Storage** - Rejected: No CDN, slow for global users, scaling issues

### Best Practices:
- **Responsive Images**: Use Cloudinary URL transformations for responsive sizes (320w, 640w, 1024w, 1920w)
- **Format Optimization**: Auto-convert to WebP for browsers that support it
- **Lazy Loading**: Use `loading="lazy"` attribute + Cloudinary's lazy load plugin
- **Product Images**: Store multiple images per product (main, gallery, thumbnails)
- **Image Naming**: Use descriptive names with product ID (product-123-main.jpg)
- **Backup**: Enable automatic backup to external storage (AWS S3) for disaster recovery

### Implementation Notes:
```typescript
// Frontend: cloudinary-react or direct URL generation
// Product images: https://res.cloudinary.com/{cloud}/image/upload/w_640,f_auto,q_auto/products/product-123-main.jpg
// Transformations: w_640 (width), f_auto (format), q_auto (quality)
```

### Image Upload Flow:
1. Admin uploads product images via Cloudinary Upload Widget
2. Cloudinary returns image URL and public_id
3. Store public_id in MongoDB product document
4. Frontend generates responsive URLs with transformations

---

## 6. MongoDB ODM: Motor (async driver) with Pydantic Validation

### Decision: **Motor** (async MongoDB driver) + **Pydantic** (validation)

### Rationale:
- **Motor**: Official async MongoDB driver for Python, works seamlessly with FastAPI's async/await
- **Pydantic**: Type-safe validation, auto-generates JSON schemas, integrates with FastAPI
- **No Heavy ODM**: Avoid Mongoengine/MongoEngine (synchronous, heavyweight, outdated patterns)
- **Direct Control**: Repository pattern with Motor gives full control over queries and aggregations

### Alternatives Considered:
1. **Mongoengine** - Rejected: Synchronous (blocks async FastAPI), outdated, heavy abstraction
2. **Beanie** - Considered: Async ODM built on Motor + Pydantic, but adds unnecessary abstraction layer
3. **PyMongo** - Rejected: Synchronous driver, would block FastAPI's async event loop

### Best Practices:
- **Repository Pattern**: Create repository classes for each collection (UserRepository, ProductRepository)
- **Pydantic Models**: Define separate models for request, response, and database documents
- **Indexes**: Create indexes in startup script (indexes.py)
- **Connection Pooling**: Configure motor client with max_pool_size=50, min_pool_size=10
- **Transactions**: Use sessions for multi-document transactions (order creation + inventory update)
- **Aggregation Pipelines**: Use for complex queries (product filtering, order stats)

### Implementation Notes:
```python
# backend/src/db/mongodb.py - Motor client setup
# backend/src/repositories/*.py - Repository pattern
# backend/src/models/*.py - Pydantic models (validation + serialization)
```

### MongoDB Best Practices:
- Use `_id` as primary key (ObjectId)
- Create compound indexes for multi-field queries (e.g., category + price)
- Use projection to fetch only required fields
- Implement pagination with skip + limit (default 20, max 100)
- Use `find_one_and_update` for atomic updates (cart items)

---

## 7. Authentication Strategy: JWT with httpOnly Cookies + Refresh Tokens

### Decision: **JWT** (JSON Web Tokens) with **httpOnly cookies** and **refresh token rotation**

### Rationale:
- **JWT**: Stateless authentication, no server-side session storage, scalable
- **httpOnly Cookies**: Prevents XSS attacks (JavaScript can't access tokens)
- **Refresh Tokens**: Long-lived (7 days) for persistent login, short-lived access tokens (15 min) for security
- **Token Rotation**: Refresh tokens are rotated on each use (prevents replay attacks)

### Alternatives Considered:
1. **Session-Based Auth** - Rejected: Requires Redis/session store, not stateless, harder to scale
2. **JWT in localStorage** - Rejected: Vulnerable to XSS attacks, tokens accessible to JavaScript
3. **OAuth2 with Third-Party** - Deferred to later: Adds complexity, requires Google/Facebook app setup

### Best Practices:
- **Access Token**: Short-lived (15 minutes), contains user ID and email
- **Refresh Token**: Long-lived (7 days), stored in httpOnly cookie, rotated on each use
- **Token Storage**: Access token in httpOnly cookie OR Authorization header (support both)
- **CSRF Protection**: Use SameSite=Strict cookie attribute + CSRF tokens for state-changing operations
- **Logout**: Blacklist refresh tokens (store in MongoDB or Redis with expiry)
- **Rate Limiting**: Limit login attempts (5 attempts, 15-minute lockout)

### Implementation Notes:
```python
# backend/src/core/security.py - JWT generation and verification
# Access token: 15 minutes expiry, contains user_id, email, is_verified
# Refresh token: 7 days expiry, random UUID, stored in database
# Cookies: httpOnly, Secure, SameSite=Strict
```

### JWT Claims:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "is_verified": true,
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Authentication Flow:
1. User logs in with email + password
2. Backend verifies credentials, generates access token (15min) and refresh token (7 days)
3. Both tokens stored in httpOnly cookies
4. Frontend sends requests with cookies (automatic)
5. Backend verifies access token on each request
6. When access token expires, frontend calls /api/auth/refresh with refresh token
7. Backend validates refresh token, generates new access + refresh tokens, rotates old refresh token

---

## 8. Cart Persistence: localStorage for Guests, MongoDB for Authenticated Users

### Decision: **Hybrid Approach** - localStorage (guests) + MongoDB (authenticated users)

### Rationale:
- **Guest Users**: Can't store in database (no account), localStorage persists across sessions (7-day expiry)
- **Authenticated Users**: Store in MongoDB for cross-device sync and reliability
- **Migration**: When guest logs in, merge localStorage cart with MongoDB cart

### Alternatives Considered:
1. **Session-Based Cart (Server)** - Rejected: Requires session management, not stateless
2. **Cookies Only** - Rejected: Size limit (4KB), not suitable for large carts
3. **IndexedDB** - Rejected: Overkill for simple cart data, localStorage is sufficient

### Best Practices:
- **localStorage Key**: `ecommerce-cart` (store cart items as JSON array)
- **Expiry**: Add `expires_at` timestamp (7 days), clear expired carts on load
- **Sync Strategy**: On login, merge localStorage cart with MongoDB cart (deduplicate by product_id)
- **Clear on Logout**: Clear localStorage cart when user logs out
- **Fallback**: If localStorage full (rare), show error and suggest reducing cart items

### Implementation Notes:
```typescript
// frontend/src/services/storage/localStorage.ts
// Methods: getCart(), setCart(), clearCart(), mergeCart()
// Structure: { items: CartItem[], expires_at: timestamp }
```

### Cart Merge Logic (Guest → Authenticated):
1. User logs in
2. Fetch localStorage cart
3. Fetch MongoDB cart for user
4. Merge carts:
   - If product exists in both, use max quantity
   - If product only in localStorage, add to MongoDB cart
   - If product only in MongoDB, keep as-is
5. Save merged cart to MongoDB
6. Clear localStorage cart
7. Update frontend cart state

---

## 9. API Design Patterns: RESTful Conventions & Pagination Strategies

### Decision: **RESTful API** with **cursor-based pagination** for large datasets

### Rationale:
- **RESTful**: Industry standard, predictable URL structure, HTTP methods map to CRUD
- **Cursor Pagination**: Better performance for large datasets (no SKIP, uses indexed fields), prevents missed/duplicate items
- **Offset Pagination**: Simpler for small datasets (products, orders), acceptable for <10k records

### Alternatives Considered:
1. **GraphQL** - Rejected: Overkill for simple CRUD, increases complexity, requires frontend query management
2. **RPC-Style** - Rejected: Less conventional, harder to cache, non-standard

### REST API Design Principles:
- **Resource-Based URLs**: `/api/products`, `/api/cart`, `/api/orders` (plural nouns)
- **HTTP Methods**: GET (read), POST (create), PATCH (update), DELETE (delete)
- **Status Codes**: 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)
- **Consistent Response Format**:
  ```json
  {
    "data": {...},
    "meta": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "has_next": true
    }
  }
  ```
- **Error Response Format**:
  ```json
  {
    "error": {
      "code": "INVALID_INPUT",
      "message": "Invalid email format",
      "details": {
        "field": "email",
        "value": "invalid"
      }
    }
  }
  ```

### Pagination Strategies:

**Offset Pagination** (simple, for small datasets):
```
GET /api/products?page=1&limit=20
Response: { data: [...], meta: { page: 1, limit: 20, total: 100, has_next: true } }
```

**Cursor Pagination** (performant, for large datasets):
```
GET /api/products?cursor=abc123&limit=20
Response: { data: [...], meta: { next_cursor: "xyz789", has_next: true } }
```

Use offset for products (max 10k), cursor for reviews/orders (unlimited).

### Filtering & Sorting:
```
# Filtering
GET /api/products?category=electronics&min_price=50&max_price=500&in_stock=true

# Sorting
GET /api/products?sort_by=price&order=asc

# Search
GET /api/products?q=laptop&fields=name,description

# Combined
GET /api/products?category=electronics&q=laptop&sort_by=price&order=asc&page=1&limit=20
```

---

## 10. Animation Patterns: GSAP Timeline Recipes

### Decision: **GSAP Timeline-based animations** with **GPU-accelerated properties**

### Rationale:
- **Performance**: GPU-accelerated (transform, opacity), 60fps on most devices
- **Control**: Timeline provides precise control over complex sequences
- **Cleanup**: Easy to kill animations on unmount (prevent memory leaks)
- **Accessibility**: Built-in support for `prefers-reduced-motion`

### Common Animation Patterns:

**1. Page Transition (Fade In)**:
```typescript
useEffect(() => {
  const tl = gsap.timeline();
  tl.from('.page', { opacity: 0, y: 20, duration: 0.5, ease: 'power2.out' });
  return () => tl.kill();
}, []);
```

**2. Product Card Hover**:
```typescript
const handleHover = (e: MouseEvent) => {
  gsap.to(e.currentTarget, { y: -10, scale: 1.05, duration: 0.3, ease: 'power2.out' });
};
const handleLeave = (e: MouseEvent) => {
  gsap.to(e.currentTarget, { y: 0, scale: 1, duration: 0.3, ease: 'power2.out' });
};
```

**3. Cart Icon Bounce (Add to Cart)**:
```typescript
const animateCartIcon = () => {
  gsap.timeline()
    .to('.cart-icon', { scale: 1.3, duration: 0.2, ease: 'back.out(1.7)' })
    .to('.cart-icon', { scale: 1, duration: 0.2, ease: 'back.out(1.7)' });
};
```

**4. Cart Item Removal (Fade Out + Slide)**:
```typescript
const removeItem = (itemId: string) => {
  gsap.timeline()
    .to(`#item-${itemId}`, { x: 100, opacity: 0, duration: 0.3, ease: 'power2.in' })
    .call(() => dispatch({ type: 'REMOVE_ITEM', itemId }));
};
```

**5. Checkout Step Transition**:
```typescript
const goToNextStep = () => {
  gsap.timeline()
    .to('.current-step', { x: -100, opacity: 0, duration: 0.3, ease: 'power2.in' })
    .call(() => setCurrentStep(step + 1))
    .from('.next-step', { x: 100, opacity: 0, duration: 0.3, ease: 'power2.out' });
};
```

**6. Loading Spinner (Infinite Rotation)**:
```typescript
useEffect(() => {
  const tl = gsap.to('.spinner', { rotation: 360, duration: 1, repeat: -1, ease: 'linear' });
  return () => tl.kill();
}, []);
```

**7. Success Confetti (Payment Success)**:
```typescript
const showSuccessConfetti = () => {
  gsap.timeline()
    .from('.success-icon', { scale: 0, rotation: -180, duration: 0.5, ease: 'back.out(1.7)' })
    .from('.confetti', { y: -100, opacity: 0, stagger: 0.05, duration: 0.5, ease: 'power2.out' }, '-=0.3');
};
```

### Accessibility - Reduced Motion:
```typescript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // Instant transitions instead of animations
  gsap.set('.element', { opacity: 1, y: 0 });
} else {
  // Normal animations
  gsap.from('.element', { opacity: 0, y: 20, duration: 0.5 });
}
```

---

## 11. Additional Best Practices

### Frontend Performance:
- **Code Splitting**: Lazy load routes with `React.lazy()` and `Suspense`
- **Image Optimization**: WebP format, responsive sizes, lazy loading with `loading="lazy"`
- **Bundle Analysis**: Use `vite-bundle-visualizer` to identify large dependencies
- **Tree Shaking**: Use ES modules, avoid CommonJS imports
- **Memoization**: Use `React.memo`, `useMemo`, `useCallback` for expensive operations

### Backend Performance:
- **Database Indexes**: Create indexes on frequently queried fields
- **Connection Pooling**: Configure Motor with appropriate pool size
- **Caching**: Use Redis for frequently accessed data (product catalog, categories)
- **Async Operations**: Use `async/await` throughout, avoid blocking operations
- **Rate Limiting**: Implement token bucket algorithm (slowapi library)

### Security:
- **Input Validation**: Validate all inputs with Pydantic (backend) and Zod (frontend)
- **SQL Injection**: Motor driver prevents this, but avoid raw queries
- **XSS Prevention**: Sanitize user-generated content, use CSP headers
- **CSRF Protection**: SameSite cookies + CSRF tokens
- **Password Security**: bcrypt with 12+ rounds, enforce strong passwords
- **HTTPS**: Enforce HTTPS in production, redirect HTTP to HTTPS

### Testing:
- **Unit Tests**: Test pure functions, hooks, services (aim for >80% coverage)
- **Integration Tests**: Test API endpoints end-to-end
- **E2E Tests**: Test critical user flows (signup, login, checkout, payment)
- **Test Data**: Use factories/fixtures for consistent test data
- **Mocking**: Mock external services (Stripe, SendGrid) in tests

---

## Technology Stack Summary

### Frontend:
- **Framework**: React 18.2+ with TypeScript 5.3+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3.4+
- **Animations**: GSAP 3.12+
- **Routing**: React Router 6+
- **HTTP Client**: Axios 1+
- **State Management**: Context API (+ Zustand if needed)
- **Form Handling**: React Hook Form + Zod
- **Testing**: Vitest + React Testing Library + Playwright

### Backend:
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: MongoDB 7+ (Motor async driver)
- **Validation**: Pydantic 2+
- **Authentication**: PyJWT 2+
- **Password Hashing**: bcrypt
- **Testing**: pytest + pytest-asyncio + httpx

### Infrastructure:
- **Database**: MongoDB Atlas (cloud) or self-hosted MongoDB
- **CDN/Images**: Cloudinary
- **Email**: SendGrid
- **Payments**: Stripe
- **Hosting**: Vercel/Netlify (frontend), AWS ECS/Google Cloud Run (backend)
- **Monitoring**: Sentry (error tracking)

---

## Next Steps

1. ✅ Research complete
2. 🎯 Create data-model.md (MongoDB schemas)
3. 🎯 Create API contracts (OpenAPI specs)
4. 🎯 Create quickstart.md (setup guide)
5. 🎯 Generate tasks with `/sp.tasks`

---

**Research Status**: ✅ COMPLETE
