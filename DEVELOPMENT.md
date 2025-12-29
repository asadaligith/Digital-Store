# E-Commerce Store - Development Documentation

> **Status**: Phase 3 Complete - Browse Products Feature Fully Functional
>
> **Last Updated**: December 29, 2025

## 📋 Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Features Implemented](#features-implemented)
6. [API Documentation](#api-documentation)
7. [Frontend Components](#frontend-components)
8. [Database Schema](#database-schema)
9. [Testing Guide](#testing-guide)
10. [Deployment](#deployment)
11. [Next Steps](#next-steps)

---

## Overview

A modern, full-stack e-commerce platform built with FastAPI (backend) and React + TypeScript (frontend). The application features product browsing, filtering, shopping cart, checkout, payment processing, and user account management.

### Current Implementation Status

✅ **Phase 1**: Project Setup (Complete)
✅ **Phase 2**: Foundational Infrastructure (Complete)
✅ **Phase 3**: Browse Products Feature (Complete)
⏳ **Phase 4**: Shopping Cart (Pending)
⏳ **Phase 5**: Checkout (Pending)
⏳ **Phase 6**: Payment (Pending)
⏳ **Phase 7**: User Accounts (Pending)
⏳ **Phase 8**: Polish & Cross-Cutting (Pending)

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: MongoDB 7.0 (Motor async driver)
- **Validation**: Pydantic 2.5+
- **Authentication**: JWT with httpOnly cookies
- **Security**: bcrypt password hashing (≥12 rounds)
- **API Docs**: OpenAPI/Swagger (auto-generated)

### Frontend
- **Framework**: React 18.2+ with TypeScript 5.3+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3.4+
- **Animations**: GSAP 3.12+
- **Routing**: React Router 6+
- **HTTP Client**: Axios
- **Form Handling**: React Hook Form + Zod

### Infrastructure
- **Database**: MongoDB (Docker containerized)
- **Code Quality**: ESLint, Prettier, Black, Ruff, mypy
- **Version Control**: Git

---

## Project Structure

```
Digital-Store/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API layer
│   │   │   ├── dependencies/  # Dependency injection
│   │   │   │   ├── auth.py           # JWT authentication
│   │   │   │   └── rate_limit.py     # Rate limiting
│   │   │   ├── middleware/    # Middleware
│   │   │   │   ├── cors.py           # CORS configuration
│   │   │   │   ├── error_handler.py  # Global error handling
│   │   │   │   └── logger.py         # Request logging
│   │   │   └── routes/        # API routes
│   │   │       ├── products.py       # Product endpoints
│   │   │       └── categories.py     # Category endpoints
│   │   ├── core/              # Core utilities
│   │   │   ├── config.py             # Settings (Pydantic)
│   │   │   ├── security.py           # JWT & password hashing
│   │   │   └── exceptions.py         # Custom exceptions
│   │   ├── db/                # Database
│   │   │   ├── mongodb.py            # MongoDB connection
│   │   │   └── indexes.py            # Index creation
│   │   ├── models/            # Pydantic models
│   │   │   ├── product.py            # Product model
│   │   │   └── category.py           # Category model
│   │   ├── schemas/           # API schemas
│   │   │   ├── product.py            # Product request/response
│   │   │   └── category.py           # Category request/response
│   │   ├── repositories/      # Data access layer
│   │   │   ├── product_repository.py
│   │   │   └── category_repository.py
│   │   ├── services/          # Business logic layer
│   │   │   ├── product_service.py
│   │   │   └── category_service.py
│   │   ├── scripts/           # Utility scripts
│   │   │   └── seed_data.py          # Database seeding
│   │   └── main.py            # Application entry point
│   ├── requirements.txt       # Python dependencies
│   └── pyproject.toml         # Tool configuration
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── common/        # Reusable components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   └── Pagination.tsx
│   │   │   ├── layout/        # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── products/      # Product components
│   │   │       ├── ProductCard.tsx
│   │   │       ├── ProductGrid.tsx
│   │   │       ├── ProductFilters.tsx
│   │   │       └── ProductSort.tsx
│   │   ├── hooks/             # Custom hooks
│   │   │   └── useAnimations.ts      # GSAP animations
│   │   ├── pages/             # Page components
│   │   │   ├── Products.tsx          # Product listing
│   │   │   └── ProductDetail.tsx     # Product detail
│   │   ├── services/          # API services
│   │   │   └── api/
│   │   │       ├── client.ts         # Axios client
│   │   │       ├── products.ts       # Product API
│   │   │       └── categories.ts     # Category API
│   │   ├── styles/            # Global styles
│   │   │   └── index.css             # Tailwind + custom
│   │   ├── types/             # TypeScript types
│   │   │   └── api.ts                # API types
│   │   ├── App.tsx            # Root component
│   │   └── main.tsx           # Entry point
│   ├── package.json           # npm dependencies
│   ├── tailwind.config.js     # Tailwind configuration
│   └── tsconfig.json          # TypeScript configuration
│
├── docker-compose.yml         # MongoDB container
└── .gitignore                 # Git ignore rules
```

---

## Getting Started

### Prerequisites

- **Python**: 3.11+
- **Node.js**: 18+ with npm
- **Docker**: For MongoDB (or local MongoDB installation)
- **Git**: Version control

### 1. Clone Repository

```bash
git clone <repository-url>
cd Digital-Store
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

**Required Environment Variables** (`.env`):
```env
# MongoDB
MONGODB_URI=mongodb://admin:password123@localhost:27017/ecommerce?authSource=admin

# JWT Secrets (generate strong random strings)
JWT_SECRET_KEY=your-secret-key-here
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# External Services (for future phases)
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG...
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your configuration
```

**Required Environment Variables** (`.env`):
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Start MongoDB

```bash
# From project root
docker-compose up -d

# Verify MongoDB is running
docker ps
```

### 5. Seed Database

```bash
cd backend
python -m src.scripts.seed_data
```

This creates:
- 5 categories (Electronics, Clothing, Books, Home & Garden, Sports)
- 20+ sample products with realistic data
- 1 admin user (email: `admin@ecommerce.com`, password: `Admin123!`)

### 6. Start Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### 7. Access Application

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/api/docs
- **Backend ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

---

## Features Implemented

### ✅ User Story 1: Browse Products

**As a customer, I want to browse and filter products so I can find items I'm interested in.**

#### Features

1. **Product Listing** (`/products`)
   - Responsive grid layout (1-4 columns based on screen size)
   - 20 products per page with pagination
   - Loading states and error handling
   - Empty state messaging

2. **Product Filtering**
   - **Category**: Filter by product category
   - **Price Range**: Min/max price filters
   - **Rating**: Minimum rating filter (1-5 stars)
   - **Stock Status**: Show only in-stock products
   - **Clear All**: Reset all filters

3. **Product Sorting**
   - Newest first (default)
   - Price: Low to High / High to Low
   - Name: A-Z / Z-A
   - Highest Rated
   - Most Popular (by review count)

4. **Product Display**
   - Product image with hover zoom
   - Product name and description
   - Current price and compare-at price
   - Discount percentage badge
   - Star rating (0-5) with review count
   - Stock status indicator
   - Featured badge
   - Add to Cart button (disabled when out of stock)

5. **Product Detail Page** (`/products/:slug`)
   - Image gallery with thumbnails
   - Full product information
   - Quantity selector
   - Stock availability
   - Breadcrumb navigation
   - Add to Cart (UI ready)

6. **Search** (UI ready, backend supports text search)
   - Search in product names and descriptions
   - Query parameter: `?search=keyword`

7. **URL Parameters** (shareable links)
   - All filters, sorting, and pagination preserved in URL
   - Examples:
     - `/products?category=electronics&sort=price:asc`
     - `/products?min_price=50&max_price=200&page=2`

#### Technical Features

- **GSAP Animations**:
  - Product card hover effect (lift + scale)
  - Stagger animation on grid load
  - Smooth transitions

- **Responsive Design**:
  - Mobile-first approach (320px baseline)
  - Breakpoints: 640px, 768px, 1024px, 1280px, 1536px
  - Touch-friendly targets (≥44px)
  - Collapsible filters on mobile

- **Accessibility**:
  - ARIA labels on all interactive elements
  - Keyboard navigation support
  - Screen reader friendly
  - Focus visible states

- **Performance**:
  - Lazy loading images
  - GPU-accelerated animations (transform/opacity only)
  - Pagination for large datasets
  - Efficient MongoDB queries with indexes

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication

Most endpoints are public. Admin endpoints require JWT authentication.

**Auth Header**:
```
Authorization: Bearer <access_token>
```

Or use httpOnly cookies (automatic with `withCredentials: true`).

---

### Product Endpoints

#### `GET /api/products`

Get paginated list of products with filtering and sorting.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `limit` | integer | 20 | Items per page (max 100) |
| `search` | string | - | Search term (name/description) |
| `category_id` | string | - | Filter by category |
| `min_price` | float | - | Minimum price |
| `max_price` | float | - | Maximum price |
| `min_rating` | float | - | Minimum rating (0-5) |
| `is_featured` | boolean | - | Featured products only |
| `in_stock_only` | boolean | - | In-stock products only |
| `sort_by` | string | created_at | Field to sort by |
| `sort_order` | string | desc | Sort order (asc/desc) |

**Response** (200 OK):
```json
{
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "Wireless Bluetooth Headphones",
      "slug": "wireless-bluetooth-headphones",
      "description": "Premium noise-cancelling wireless headphones...",
      "category_id": "electronics",
      "price": 129.99,
      "compare_at_price": 199.99,
      "sku": "ELEC-HEAD-001",
      "inventory_quantity": 50,
      "images": ["https://..."],
      "is_featured": true,
      "is_active": true,
      "rating": 4.5,
      "review_count": 128,
      "discount_percentage": 35.0,
      "is_in_stock": true,
      "is_low_stock": false,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 42,
    "pages": 3
  }
}
```

---

#### `GET /api/products/featured`

Get featured products.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 8 | Number of products (max 50) |

---

#### `GET /api/products/category/{category_id}`

Get products by category.

**Path Parameters**:
- `category_id`: Category identifier

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20)

---

#### `GET /api/products/{product_id}`

Get product by ID.

**Path Parameters**:
- `product_id`: MongoDB ObjectId

**Response** (200 OK): Product object

---

#### `GET /api/products/slug/{slug}`

Get product by URL slug.

**Path Parameters**:
- `slug`: Product slug (e.g., "wireless-bluetooth-headphones")

**Response** (200 OK): Product object

---

#### `POST /api/products` 🔒 Admin Only

Create a new product.

**Request Body**:
```json
{
  "name": "Product Name",
  "slug": "product-name",
  "description": "Product description",
  "category_id": "electronics",
  "price": 99.99,
  "compare_at_price": 149.99,
  "sku": "SKU-001",
  "inventory_quantity": 100,
  "images": ["https://..."],
  "is_featured": false,
  "is_active": true
}
```

---

#### `PUT /api/products/{product_id}` 🔒 Admin Only

Update a product.

**Request Body**: Same as create (all fields optional)

---

#### `DELETE /api/products/{product_id}` 🔒 Admin Only

Delete a product.

**Response** (204 No Content)

---

### Category Endpoints

#### `GET /api/categories`

Get all categories with product counts.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `is_active` | boolean | true | Filter by active status |
| `include_product_count` | boolean | true | Include product counts |

**Response** (200 OK):
```json
{
  "data": [
    {
      "_id": "electronics",
      "name": "Electronics",
      "slug": "electronics",
      "description": "Latest gadgets and electronic devices",
      "image_url": "https://...",
      "is_active": true,
      "product_count": 42,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

#### `GET /api/categories/{category_id}`

Get category by ID.

---

#### `GET /api/categories/slug/{slug}`

Get category by slug.

---

#### `POST /api/categories` 🔒 Admin Only

Create a category.

---

#### `PUT /api/categories/{category_id}` 🔒 Admin Only

Update a category.

---

#### `DELETE /api/categories/{category_id}` 🔒 Admin Only

Delete a category (only if no products).

---

## Frontend Components

### Common Components

#### Button
```tsx
<Button
  variant="primary|secondary|outline|ghost|danger"
  size="sm|md|lg"
  isLoading={false}
  disabled={false}
  fullWidth={false}
  leftIcon={<Icon />}
  rightIcon={<Icon />}
  onClick={handleClick}
>
  Button Text
</Button>
```

#### Input
```tsx
<Input
  label="Email"
  type="email"
  placeholder="you@example.com"
  error={errors.email}
  helperText="We'll never share your email"
  required
  leftIcon={<Icon />}
  size="sm|md|lg"
/>
```

#### Modal
```tsx
<Modal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  title="Modal Title"
  size="sm|md|lg|xl|full"
  footer={<Button>Action</Button>}
  closeOnBackdropClick={true}
  closeOnEscape={true}
>
  Modal content
</Modal>
```

#### Pagination
```tsx
<Pagination
  currentPage={1}
  totalPages={10}
  onPageChange={setPage}
  maxButtons={7}
/>
```

### Product Components

#### ProductCard
```tsx
<ProductCard
  product={product}
  onAddToCart={handleAddToCart}
/>
```

#### ProductGrid
```tsx
<ProductGrid
  products={products}
  isLoading={isLoading}
  onAddToCart={handleAddToCart}
/>
```

#### ProductFilters
```tsx
<ProductFilters
  categories={categories}
  filters={filters}
  onFiltersChange={setFilters}
  onClearFilters={clearFilters}
/>
```

### Custom Hooks

#### useAnimations
```tsx
const { fadeIn, slideIn, cardHover, staggerIn } = useAnimations();

// Fade in
fadeIn('.element', { duration: 0.5 });

// Slide in
slideIn('.element', { direction: 'up', distance: 50 });

// Card hover
cardHover(cardRef.current, isHovering);

// Stagger animation
staggerIn('.items', { stagger: 0.1 });
```

---

## Database Schema

### Products Collection

```javascript
{
  _id: ObjectId,
  name: string,
  slug: string (unique),
  description: string,
  category_id: string,
  price: number,
  compare_at_price: number?,
  sku: string (unique),
  inventory_quantity: number,
  images: string[],
  is_featured: boolean,
  is_active: boolean,
  rating: number (0-5),
  review_count: number,
  created_at: datetime,
  updated_at: datetime
}
```

**Indexes**:
- `slug` (unique)
- `sku` (unique)
- `category_id, price` (compound)
- `name, description` (text search)

### Categories Collection

```javascript
{
  _id: string (custom ID),
  name: string,
  slug: string (unique),
  description: string,
  image_url: string?,
  icon: string?,
  is_active: boolean,
  created_at: datetime,
  updated_at: datetime
}
```

**Indexes**:
- `slug` (unique)
- `is_active`

---

## Testing Guide

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_products.py

# Run with verbose output
pytest -v
```

### Frontend Testing

```bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Run e2e tests (Playwright)
npm run test:e2e

# Open test UI
npm run test:ui
```

### Manual Testing Checklist

**Product Browsing**:
- [ ] Load products page - verify 20 products displayed
- [ ] Apply category filter - verify results update
- [ ] Set price range - verify filtering works
- [ ] Change sort order - verify products re-order
- [ ] Navigate to page 2 - verify pagination
- [ ] Click product - verify detail page loads
- [ ] Search for product - verify results
- [ ] Test on mobile - verify responsive layout

**API Testing**:
- [ ] Visit `/api/docs` - verify Swagger UI loads
- [ ] Test GET /api/products - verify response
- [ ] Test filtering - verify query params work
- [ ] Test pagination - verify meta data
- [ ] Test GET /api/categories - verify categories load

---

## Deployment

### Backend Deployment (Production)

1. **Environment Variables**: Set all required env vars
2. **Database**: MongoDB Atlas or managed instance
3. **Secrets**: Use secure secret manager
4. **CORS**: Update allowed origins
5. **Run**: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

**Recommended Platforms**:
- Railway
- Render
- Fly.io
- AWS EC2 + ECS

### Frontend Deployment

1. **Build**: `npm run build`
2. **Output**: `dist/` directory
3. **Environment**: Set `VITE_API_BASE_URL`

**Recommended Platforms**:
- Vercel
- Netlify
- Cloudflare Pages
- AWS S3 + CloudFront

---

## Next Steps

### Phase 4: Shopping Cart

**Features to Implement**:
- Cart model and backend API
- Cart context/state management
- Cart page with item list
- Cart sidebar/dropdown
- Add/remove/update quantities
- Persist cart to backend
- Cart badge on header

**Estimated Effort**: 23 tasks

### Phase 5: Checkout

**Features to Implement**:
- Checkout page and flow
- Shipping address form
- Order summary
- Order creation
- Email confirmation

**Estimated Effort**: 23 tasks

### Phase 6: Payment

**Features to Implement**:
- Stripe integration
- Payment form
- Payment processing
- Order status tracking
- Receipt generation

**Estimated Effort**: 30 tasks

---

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Follow code style (run linters)
3. Write tests for new features
4. Update documentation
5. Submit pull request

## License

[Your License Here]

## Support

For issues or questions, please contact: [Your Contact]
