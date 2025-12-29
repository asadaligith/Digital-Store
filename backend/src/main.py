"""
FastAPI application entry point.

This is the main application file that initializes FastAPI,
registers middleware, routes, and event handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.core.config import settings, validate_settings
from src.db.mongodb import connect_to_mongo, close_mongo_connection, get_database
from src.db.indexes import create_indexes
from src.api.middleware.cors import setup_cors
from src.api.middleware.error_handler import error_handler_middleware
from src.api.middleware.logger import logger_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events:
    - Startup: Connect to MongoDB, create indexes, validate configuration
    - Shutdown: Close database connection
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📝 Environment: {settings.ENVIRONMENT}")

    try:
        # Validate configuration
        validate_settings()

        # Connect to MongoDB
        await connect_to_mongo(settings.MONGODB_URI)

        # Create database indexes
        await create_indexes(get_database())

        print(f"✅ {settings.APP_NAME} started successfully!")

    except Exception as e:
        print(f"❌ Startup failed: {str(e)}")
        raise

    yield

    # Shutdown
    print(f"🛑 Shutting down {settings.APP_NAME}...")
    await close_mongo_connection()
    print("👋 Shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# ===== Middleware (order matters!) =====

# 1. CORS - Must be first to handle preflight requests
setup_cors(app)

# 2. Logger - Log all requests
app.middleware("http")(logger_middleware)

# 3. Error Handler - Catch all exceptions
app.middleware("http")(error_handler_middleware)

# ===== Routes =====

from src.api.routes import products, categories

app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])

# Note: Additional routes will be added as we implement each feature
# Example:
# from src.api.routes import auth, cart, orders, users
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
# app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
# app.include_router(users.router, prefix="/api/users", tags=["Users"])

# ===== Health Check =====

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        200 OK with status information
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Returns:
        API metadata and documentation links
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": f"{str(app.url_path_for('swagger_ui_html'))}",
        "health": "/health"
    }
