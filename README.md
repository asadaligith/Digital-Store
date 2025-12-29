# E-Commerce Store

A modern, full-stack e-commerce platform built with FastAPI and React.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for MongoDB)

### Setup

1. **Clone and navigate**:
   ```bash
   git clone <repository-url>
   cd Digital-Store
   ```

2. **Start MongoDB**:
   ```bash
   docker-compose up -d
   ```

3. **Setup Backend**:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   cp .env.example .env  # Edit with your settings
   python -m src.scripts.seed_data
   ```

4. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   cp .env.example .env  # Edit with your settings
   ```

5. **Run Development Servers**:

   **Terminal 1 - Backend**:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

   **Terminal 2 - Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

6. **Access**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/docs
   - Health Check: http://localhost:8000/health

## 📚 Documentation

See [DEVELOPMENT.md](./DEVELOPMENT.md) for comprehensive documentation including:
- Project structure
- API endpoints
- Component documentation
- Database schema
- Testing guide
- Deployment instructions

## ✨ Features

### ✅ Implemented (Phase 1-3)

- **Product Browsing**
  - Responsive product grid (1-4 columns)
  - Advanced filtering (category, price, rating, stock)
  - Multiple sort options
  - Pagination
  - Search functionality
  - Product detail pages with image galleries

- **Backend API**
  - RESTful API with FastAPI
  - MongoDB with async Motor driver
  - JWT authentication (infrastructure ready)
  - Rate limiting
  - Comprehensive error handling
  - Auto-generated API docs

- **Frontend**
  - React 18 + TypeScript
  - Tailwind CSS styling
  - GSAP animations
  - Responsive design (mobile-first)
  - Accessibility (ARIA, keyboard navigation)
  - Touch-friendly (≥44px targets)

### 🔜 Coming Soon (Phase 4-8)

- Shopping Cart
- Checkout Flow
- Payment Processing (Stripe)
- User Authentication & Accounts
- Order Management
- Admin Dashboard

## 🗂️ Project Structure

```
Digital-Store/
├── backend/           # FastAPI backend
│   ├── src/
│   │   ├── api/      # API routes & middleware
│   │   ├── models/   # Pydantic models
│   │   ├── services/ # Business logic
│   │   └── db/       # Database layer
│   └── requirements.txt
│
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── hooks/       # Custom hooks
│   └── package.json
│
└── docker-compose.yml # MongoDB container
```

## 🛠️ Tech Stack

**Backend**: FastAPI · MongoDB · Pydantic · JWT · bcrypt

**Frontend**: React · TypeScript · Tailwind CSS · GSAP · Vite

**Infrastructure**: Docker · MongoDB Atlas (production)

## 📊 Current Status

| Phase | Status | Progress |
|-------|--------|----------|
| 1. Setup | ✅ Complete | 100% |
| 2. Infrastructure | ✅ Complete | 100% |
| 3. Browse Products | ✅ Complete | 100% |
| 4. Shopping Cart | ⏳ Pending | 0% |
| 5. Checkout | ⏳ Pending | 0% |
| 6. Payment | ⏳ Pending | 0% |
| 7. User Accounts | ⏳ Pending | 0% |
| 8. Polish | ⏳ Pending | 0% |

**Overall Progress**: 37.5% (3/8 phases complete)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest --cov=src

# Frontend tests
cd frontend
npm test
npm run test:e2e
```

## 🎯 Sample Data

The seed script creates:
- 5 product categories
- 20+ sample products
- 1 admin user (`admin@ecommerce.com` / `Admin123!`)

Run seeding:
```bash
cd backend
python -m src.scripts.seed_data
```

## 📖 API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

- `GET /api/products` - List products (with filtering/sorting)
- `GET /api/products/{id}` - Get product details
- `GET /api/products/slug/{slug}` - Get product by slug
- `GET /api/categories` - List categories
- `GET /health` - Health check

See [DEVELOPMENT.md](./DEVELOPMENT.md) for complete API reference.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

[Your License Here]

## 💬 Support

For questions or issues:
- 📧 Email: [Your Email]
- 🐛 Issues: [GitHub Issues]
- 📚 Docs: [DEVELOPMENT.md](./DEVELOPMENT.md)

---

**Built with ❤️ using FastAPI and React**
