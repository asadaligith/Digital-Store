# Quickstart Guide: E-Commerce Store Platform

**Feature**: E-Commerce Store Platform
**Branch**: `001-ecommerce-store`
**Date**: 2025-12-29

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Development Workflow](#development-workflow)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** ([Download](https://www.docker.com/get-started/))
- **Git** ([Download](https://git-scm.com/downloads))

### Optional (for production)

- **MongoDB Atlas Account** (free tier available: [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))
- **Stripe Account** (test mode free: [stripe.com](https://stripe.com/))
- **SendGrid Account** (100 emails/day free: [sendgrid.com](https://sendgrid.com/))
- **Cloudinary Account** (25GB free: [cloudinary.com](https://cloudinary.com/))

---

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd Digital-Store
git checkout 001-ecommerce-store
```

### 2. Backend Setup (FastAPI + MongoDB)

#### Install Dependencies

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
pip install -r requirements-dev.txt
```

#### Environment Configuration

Create `backend/.env` file:

```bash
# Copy example env file
cp .env.example .env
```

Edit `backend/.env`:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/ecommerce_db
MONGODB_DATABASE=ecommerce_db

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_REFRESH_SECRET_KEY=your-super-secret-refresh-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Stripe (test keys)
STRIPE_SECRET_KEY=sk_test_your_stripe_test_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_test_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# SendGrid
SENDGRID_API_KEY=SG.your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@example.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Rate Limiting
RATE_LIMIT_AUTHENTICATED=100  # requests per minute
RATE_LIMIT_ANONYMOUS=20       # requests per minute

# Environment
ENVIRONMENT=development  # development, staging, production
```

#### Start MongoDB with Docker

```bash
# From project root
docker-compose up -d mongodb

# Verify MongoDB is running
docker ps
```

#### Create Database Indexes

```bash
cd backend
python -m src.db.indexes
```

#### Seed Sample Data (Optional)

```bash
python -m src.scripts.seed_data
```

This creates:
- 10 categories
- 100 sample products
- 5 test users (email: `user1@test.com` to `user5@test.com`, password: `Test1234!`)

#### Run Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# The API will be available at http://localhost:8000
# API documentation (Swagger UI): http://localhost:8000/docs
# Alternative API documentation (ReDoc): http://localhost:8000/redoc
```

---

### 3. Frontend Setup (React + TypeScript + Tailwind CSS)

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Environment Configuration

Create `frontend/.env` file:

```bash
# Copy example env file
cp .env.example .env
```

Edit `frontend/.env`:

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000

# Stripe
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_test_publishable_key

# Environment
VITE_ENVIRONMENT=development
```

#### Run Frontend Server

```bash
npm run dev

# The frontend will be available at http://localhost:5173
```

---

## Development Workflow

### Running Both Frontend and Backend

**Option 1: Separate Terminals**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**Option 2: Docker Compose (Full Stack)**

From project root:
```bash
docker-compose up

# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# MongoDB: mongodb://localhost:27017
```

---

### Code Quality Tools

#### Backend (Python)

```bash
cd backend

# Format code with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type checking with mypy
mypy src/

# Run all checks
black src/ tests/ && ruff check src/ tests/ && mypy src/
```

#### Frontend (TypeScript/React)

```bash
cd frontend

# Format code with Prettier
npm run format

# Lint with ESLint
npm run lint

# Type checking
npm run type-check

# Run all checks
npm run format && npm run lint && npm run type-check
```

#### Pre-commit Hooks

Install pre-commit hooks (runs checks before every commit):

```bash
# From project root
pip install pre-commit
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

---

## Testing

### Backend Testing (pytest)

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/

# Run unit tests only
pytest tests/unit/
```

### Frontend Testing

```bash
cd frontend

# Run unit tests (Vitest)
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch

# Run E2E tests (Playwright)
npm run test:e2e

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed
```

---

## API Documentation

### Swagger UI (Interactive API Docs)

Open browser: `http://localhost:8000/docs`

- Interactive API documentation
- Try out endpoints directly
- View request/response schemas
- Test authentication

### ReDoc (Alternative API Docs)

Open browser: `http://localhost:8000/redoc`

- Clean, readable API documentation
- Better for sharing with team
- Printable format

---

## Common Development Tasks

### Add New API Endpoint

1. **Create/Update Pydantic Model** (`backend/src/models/*.py`)
2. **Create/Update Repository** (`backend/src/repositories/*.py`)
3. **Create/Update Service** (`backend/src/services/*.py`)
4. **Create/Update Route** (`backend/src/api/routes/*.py`)
5. **Write Tests** (`backend/tests/`)

Example:
```bash
# 1. Model
backend/src/models/product.py

# 2. Repository
backend/src/repositories/product_repository.py

# 3. Service
backend/src/services/product_service.py

# 4. Route
backend/src/api/routes/products.py

# 5. Tests
backend/tests/unit/test_product_service.py
backend/tests/integration/test_products_api.py
```

### Add New React Component

1. **Create Component** (`frontend/src/components/`)
2. **Create TypeScript Types** (`frontend/src/types/`)
3. **Create Tests** (`frontend/tests/component/`)
4. **Add to Storybook** (optional)

Example:
```bash
# 1. Component
frontend/src/components/products/ProductCard.tsx

# 2. Types
frontend/src/types/product.ts

# 3. Tests
frontend/tests/component/ProductCard.test.tsx
```

### Database Operations

```bash
# Connect to MongoDB (Docker)
docker exec -it mongodb mongosh

# Use database
use ecommerce_db

# Show collections
show collections

# Query products
db.products.find().limit(5)

# Create index
db.products.createIndex({ "slug": 1 }, { unique: true })

# Drop database (careful!)
db.dropDatabase()
```

### Reset Development Database

```bash
# Stop containers
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v

# Start fresh
docker-compose up -d mongodb
cd backend
python -m src.db.indexes
python -m src.scripts.seed_data
```

---

## Deployment

### Production Environment Variables

**Backend (`backend/.env.production`)**:
```env
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/ecommerce_db
JWT_SECRET_KEY=<strong-random-secret-256-bits>
JWT_REFRESH_SECRET_KEY=<strong-random-secret-256-bits>
STRIPE_SECRET_KEY=sk_live_...
SENDGRID_API_KEY=SG.live...
CORS_ORIGINS=https://example.com,https://www.example.com
ENVIRONMENT=production
```

**Frontend (`frontend/.env.production`)**:
```env
VITE_API_BASE_URL=https://api.example.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...
VITE_ENVIRONMENT=production
```

### Build for Production

**Backend (Docker)**:
```bash
cd backend
docker build -t ecommerce-backend:latest .
docker run -p 8000:8000 --env-file .env.production ecommerce-backend:latest
```

**Frontend (Static Build)**:
```bash
cd frontend
npm run build

# Output in frontend/dist/
# Deploy to Vercel, Netlify, AWS S3, etc.
```

### Deploy to Vercel (Frontend)

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

### Deploy to Google Cloud Run (Backend)

```bash
cd backend
gcloud run deploy ecommerce-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError` in Backend

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements-dev.txt
```

#### Issue: `ECONNREFUSED` when Frontend calls API

**Solution**:
1. Ensure backend is running on `http://localhost:8000`
2. Check `VITE_API_BASE_URL` in `frontend/.env`
3. Verify CORS origins in `backend/.env` include `http://localhost:5173`

#### Issue: MongoDB connection refused

**Solution**:
```bash
# Check if MongoDB container is running
docker ps

# If not running, start it
docker-compose up -d mongodb

# Check logs
docker logs mongodb
```

#### Issue: `401 Unauthorized` on protected routes

**Solution**:
1. Ensure you're sending JWT token in request headers or cookies
2. Check token expiration (access token expires in 15 minutes)
3. Use refresh token to get new access token
4. Clear cookies/localStorage and login again

#### Issue: Tailwind styles not working

**Solution**:
```bash
cd frontend
# Restart dev server
npm run dev
```

#### Issue: Tests failing

**Solution**:
```bash
# Backend: Ensure test database is clean
pytest --create-db

# Frontend: Clear test cache
npm run test:clear-cache
```

---

## Additional Resources

### Documentation Links

- **React**: https://react.dev/
- **FastAPI**: https://fastapi.tiangolo.com/
- **MongoDB**: https://www.mongodb.com/docs/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **GSAP**: https://greensock.com/docs/
- **Stripe**: https://stripe.com/docs
- **SendGrid**: https://docs.sendgrid.com/

### Project Documentation

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Research Decisions**: [research.md](./research.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/api.openapi.yaml](./contracts/api.openapi.yaml)

### Development Tools

- **VS Code Extensions**:
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)
  - ES7+ React/Redux/React-Native snippets
  - Tailwind CSS IntelliSense
  - Prettier - Code formatter
  - ESLint
  - Thunder Client (API testing)

---

## Next Steps

1. ✅ Setup complete
2. 🎯 Run `/sp.tasks` to generate detailed task breakdown
3. 🎯 Run `/sp.implement` to begin implementation

---

**Quickstart Status**: ✅ COMPLETE
