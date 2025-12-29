# E-Commerce Store - Backend

RESTful API built with FastAPI, Python, and MongoDB for a modern e-commerce platform.

## Tech Stack

- **FastAPI 0.104+** - Modern async web framework
- **Python 3.11+** - Programming language
- **MongoDB 7+** - Document database
- **Motor 3+** - Async MongoDB driver
- **Pydantic 2+** - Data validation
- **PyJWT** - JWT authentication
- **Stripe** - Payment processing
- **SendGrid** - Email service

## Prerequisites

- Python 3.11 or higher
- MongoDB 7+ (via Docker or local installation)
- Stripe account (for payment processing)
- SendGrid account (for email sending)

## Quick Start

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Start MongoDB** (using Docker):
   ```bash
   docker-compose up -d mongodb
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations** (create indexes):
   ```bash
   python -m src.db.indexes
   ```

6. **Seed sample data** (optional):
   ```bash
   python -m src.scripts.seed_data
   ```

7. **Start development server**:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Access API docs**:
   - Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
   - ReDoc: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## Project Structure

```
src/
├── api/              # API layer
│   ├── routes/      # FastAPI route handlers
│   ├── dependencies/ # Route dependencies (auth, rate limiting)
│   └── middleware/  # Custom middleware (CORS, error handling)
├── services/        # Business logic layer
├── repositories/    # Data access layer
├── models/          # Pydantic models (schemas)
├── db/              # Database configuration
├── core/            # Core utilities (config, security, exceptions)
├── utils/           # Helper functions
└── main.py          # FastAPI application entry point
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout (revoke refresh token)
- `POST /api/auth/refresh` - Refresh access token

### Products
- `GET /api/products` - List products (with filters, pagination)
- `GET /api/products/:id` - Get product by ID
- `GET /api/products/slug/:slug` - Get product by slug
- `GET /api/categories` - List categories

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/items` - Add item to cart
- `PATCH /api/cart/items/:id` - Update item quantity
- `DELETE /api/cart/items/:id` - Remove item from cart

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - List user's orders
- `GET /api/orders/:id` - Get order details

### Payments
- `POST /api/payments/process` - Process payment
- `POST /api/payments/webhook` - Stripe webhook handler

### Users
- `GET /api/users/profile` - Get user profile
- `PATCH /api/users/profile` - Update user profile
- `GET /api/users/addresses` - List saved addresses
- `POST /api/users/addresses` - Add new address

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_product_service.py
```

## Code Quality

```bash
# Format code with Black
black src tests

# Lint with Ruff
ruff check src tests --fix

# Type check with mypy
mypy src
```

## Environment Variables

See `.env.example` for all required environment variables. Key configurations:

- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET_KEY` - Secret for signing JWT tokens
- `STRIPE_SECRET_KEY` - Stripe API key
- `SENDGRID_API_KEY` - SendGrid API key
- `CORS_ORIGINS` - Allowed CORS origins

## Security

- JWT authentication with httpOnly cookies
- bcrypt password hashing (≥12 rounds)
- Rate limiting (100 req/min authenticated, 20 req/min anonymous)
- CSRF protection
- Input validation with Pydantic
- Parameterized queries (Motor driver)

## Performance

- Connection pooling (max 50, min 10)
- Database indexes on all query fields
- API response caching (optional with Redis)
- Async/await for all I/O operations

## License

Proprietary
