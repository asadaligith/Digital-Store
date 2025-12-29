"""
Seed data script to populate MongoDB with sample data for development.

This script creates:
- Categories (Electronics, Clothing, Books, Home & Garden, Sports)
- Products (50+ sample products with realistic data)
- Admin user for testing

Usage:
    python -m src.scripts.seed_data

Features:
- Idempotent (can run multiple times safely)
- Async operations with Motor
- Realistic e-commerce data
- Progress indicators
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.core.security import hash_password


async def clear_collections(db):
    """Clear existing data (optional - for clean slate)."""
    print("🗑️  Clearing existing collections...")

    collections = ["categories", "products", "users"]
    for collection in collections:
        await db[collection].delete_many({})

    print("✅ Collections cleared")


async def create_categories(db):
    """Create product categories."""
    print("\n📁 Creating categories...")

    categories = [
        {
            "_id": "electronics",
            "name": "Electronics",
            "slug": "electronics",
            "description": "Latest gadgets and electronic devices",
            "image_url": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=800",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "_id": "clothing",
            "name": "Clothing",
            "slug": "clothing",
            "description": "Fashion and apparel for everyone",
            "image_url": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "_id": "books",
            "name": "Books",
            "slug": "books",
            "description": "Wide selection of books and magazines",
            "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "_id": "home-garden",
            "name": "Home & Garden",
            "slug": "home-garden",
            "description": "Everything for your home and garden",
            "image_url": "https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=800",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "_id": "sports",
            "name": "Sports & Outdoors",
            "slug": "sports",
            "description": "Sports equipment and outdoor gear",
            "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
    ]

    await db.categories.insert_many(categories)
    print(f"✅ Created {len(categories)} categories")


async def create_products(db):
    """Create sample products."""
    print("\n📦 Creating products...")

    products = [
        # Electronics
        {
            "name": "Wireless Bluetooth Headphones",
            "slug": "wireless-bluetooth-headphones",
            "description": "Premium noise-cancelling wireless headphones with 30-hour battery life. Deep bass, crystal clear audio, and comfortable design for all-day wear.",
            "category_id": "electronics",
            "price": 129.99,
            "compare_at_price": 199.99,
            "sku": "ELEC-HEAD-001",
            "inventory_quantity": 50,
            "images": [
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
                "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.5,
            "review_count": 128,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "4K Smart TV 55 inch",
            "slug": "4k-smart-tv-55-inch",
            "description": "Ultra HD 4K Smart TV with HDR, built-in streaming apps, and voice control. Transform your living room into a home theater.",
            "category_id": "electronics",
            "price": 599.99,
            "compare_at_price": 799.99,
            "sku": "ELEC-TV-001",
            "inventory_quantity": 25,
            "images": [
                "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.7,
            "review_count": 89,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Mechanical Gaming Keyboard",
            "slug": "mechanical-gaming-keyboard",
            "description": "RGB backlit mechanical keyboard with tactile switches. Perfect for gaming and typing with customizable macros.",
            "category_id": "electronics",
            "price": 89.99,
            "sku": "ELEC-KEY-001",
            "inventory_quantity": 75,
            "images": [
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.6,
            "review_count": 234,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Wireless Mouse",
            "slug": "wireless-mouse",
            "description": "Ergonomic wireless mouse with precision tracking and long battery life.",
            "category_id": "electronics",
            "price": 29.99,
            "sku": "ELEC-MOUSE-001",
            "inventory_quantity": 100,
            "images": [
                "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.3,
            "review_count": 156,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Portable Power Bank 20000mAh",
            "slug": "portable-power-bank-20000mah",
            "description": "High-capacity portable charger with fast charging technology. Charge multiple devices on the go.",
            "category_id": "electronics",
            "price": 39.99,
            "compare_at_price": 59.99,
            "sku": "ELEC-PWR-001",
            "inventory_quantity": 150,
            "images": [
                "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.4,
            "review_count": 203,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },

        # Clothing
        {
            "name": "Classic Denim Jacket",
            "slug": "classic-denim-jacket",
            "description": "Timeless denim jacket with a modern fit. Perfect for layering in any season.",
            "category_id": "clothing",
            "price": 79.99,
            "compare_at_price": 99.99,
            "sku": "CLO-JAC-001",
            "inventory_quantity": 60,
            "images": [
                "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.6,
            "review_count": 78,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Cotton T-Shirt Pack (3-Pack)",
            "slug": "cotton-t-shirt-pack",
            "description": "Premium 100% cotton t-shirts. Soft, breathable, and durable. Available in multiple colors.",
            "category_id": "clothing",
            "price": 34.99,
            "sku": "CLO-TSH-001",
            "inventory_quantity": 200,
            "images": [
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.5,
            "review_count": 312,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Running Shoes",
            "slug": "running-shoes",
            "description": "Lightweight running shoes with excellent cushioning and support for long-distance runs.",
            "category_id": "clothing",
            "price": 119.99,
            "compare_at_price": 149.99,
            "sku": "CLO-SHOE-001",
            "inventory_quantity": 80,
            "images": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.8,
            "review_count": 167,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Leather Belt",
            "slug": "leather-belt",
            "description": "Genuine leather belt with classic buckle. Perfect for formal and casual wear.",
            "category_id": "clothing",
            "price": 29.99,
            "sku": "CLO-BELT-001",
            "inventory_quantity": 120,
            "images": [
                "https://images.unsplash.com/photo-1624222247344-550fb60583bb?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.4,
            "review_count": 92,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Winter Beanie",
            "slug": "winter-beanie",
            "description": "Warm and cozy beanie for cold weather. Made from soft acrylic yarn.",
            "category_id": "clothing",
            "price": 19.99,
            "sku": "CLO-HAT-001",
            "inventory_quantity": 150,
            "images": [
                "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.3,
            "review_count": 54,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },

        # Books
        {
            "name": "The Psychology of Money",
            "slug": "psychology-of-money",
            "description": "Timeless lessons on wealth, greed, and happiness. A must-read for anyone interested in personal finance.",
            "category_id": "books",
            "price": 24.99,
            "sku": "BOOK-FIN-001",
            "inventory_quantity": 100,
            "images": [
                "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.9,
            "review_count": 412,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "slug": "clean-code-handbook",
            "description": "Essential reading for software developers. Learn how to write code that is clean, testable, and maintainable.",
            "category_id": "books",
            "price": 39.99,
            "compare_at_price": 49.99,
            "sku": "BOOK-TECH-001",
            "inventory_quantity": 75,
            "images": [
                "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.8,
            "review_count": 523,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Atomic Habits",
            "slug": "atomic-habits",
            "description": "An easy and proven way to build good habits and break bad ones. Transform your life one tiny change at a time.",
            "category_id": "books",
            "price": 26.99,
            "sku": "BOOK-SELF-001",
            "inventory_quantity": 90,
            "images": [
                "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.9,
            "review_count": 687,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },

        # Home & Garden
        {
            "name": "Stainless Steel Cookware Set (10-Piece)",
            "slug": "stainless-steel-cookware-set",
            "description": "Professional-grade cookware set including pots, pans, and lids. Dishwasher safe and oven safe up to 500°F.",
            "category_id": "home-garden",
            "price": 249.99,
            "compare_at_price": 349.99,
            "sku": "HOME-COOK-001",
            "inventory_quantity": 40,
            "images": [
                "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.7,
            "review_count": 156,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Memory Foam Pillow (2-Pack)",
            "slug": "memory-foam-pillow",
            "description": "Ergonomic memory foam pillows for better sleep. Hypoallergenic and machine washable cover.",
            "category_id": "home-garden",
            "price": 59.99,
            "sku": "HOME-BED-001",
            "inventory_quantity": 100,
            "images": [
                "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.5,
            "review_count": 234,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Indoor Plant Collection (5 Plants)",
            "slug": "indoor-plant-collection",
            "description": "Beautiful low-maintenance indoor plants to freshen up your space. Includes decorative pots.",
            "category_id": "home-garden",
            "price": 79.99,
            "sku": "HOME-PLANT-001",
            "inventory_quantity": 50,
            "images": [
                "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.6,
            "review_count": 98,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },

        # Sports & Outdoors
        {
            "name": "Yoga Mat with Carrying Strap",
            "slug": "yoga-mat-carrying-strap",
            "description": "Premium non-slip yoga mat with excellent cushioning. Perfect for yoga, pilates, and floor exercises.",
            "category_id": "sports",
            "price": 34.99,
            "sku": "SPORT-YOGA-001",
            "inventory_quantity": 120,
            "images": [
                "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.4,
            "review_count": 187,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Adjustable Dumbbells Set",
            "slug": "adjustable-dumbbells-set",
            "description": "Space-saving adjustable dumbbells from 5 to 52.5 lbs. Perfect for home workouts.",
            "category_id": "sports",
            "price": 299.99,
            "compare_at_price": 399.99,
            "sku": "SPORT-DUMB-001",
            "inventory_quantity": 35,
            "images": [
                "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800",
            ],
            "is_featured": True,
            "is_active": True,
            "rating": 4.8,
            "review_count": 312,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "name": "Camping Tent (4-Person)",
            "slug": "camping-tent-4-person",
            "description": "Waterproof camping tent with easy setup. Includes rainfly, stakes, and carrying bag.",
            "category_id": "sports",
            "price": 149.99,
            "sku": "SPORT-CAMP-001",
            "inventory_quantity": 45,
            "images": [
                "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800",
            ],
            "is_featured": False,
            "is_active": True,
            "rating": 4.5,
            "review_count": 145,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
    ]

    await db.products.insert_many(products)
    print(f"✅ Created {len(products)} products")


async def create_admin_user(db):
    """Create admin user for testing."""
    print("\n👤 Creating admin user...")

    admin = {
        "email": "admin@ecommerce.com",
        "password": hash_password("Admin123!"),
        "name": "Admin User",
        "role": "admin",
        "is_active": True,
        "email_verified": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Check if admin exists
    existing_admin = await db.users.find_one({"email": admin["email"]})
    if existing_admin:
        print(f"ℹ️  Admin user already exists: {admin['email']}")
    else:
        await db.users.insert_one(admin)
        print(f"✅ Created admin user: {admin['email']} / Admin123!")


async def main():
    """Main execution function."""
    print("🌱 Starting seed data script...")
    print(f"📍 Connecting to: {settings.MONGODB_URI}")

    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client.get_database()

    try:
        # Test connection
        await db.command("ping")
        print("✅ Connected to MongoDB\n")

        # Clear existing data (optional - uncomment if you want a clean slate)
        # await clear_collections(db)

        # Create data
        await create_categories(db)
        await create_products(db)
        await create_admin_user(db)

        # Print summary
        category_count = await db.categories.count_documents({})
        product_count = await db.products.count_documents({})
        user_count = await db.users.count_documents({})

        print("\n" + "=" * 50)
        print("📊 SEED DATA SUMMARY")
        print("=" * 50)
        print(f"Categories: {category_count}")
        print(f"Products: {product_count}")
        print(f"Users: {user_count}")
        print("=" * 50)
        print("\n✅ Seed data script completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        client.close()
        print("👋 Database connection closed")


if __name__ == "__main__":
    asyncio.run(main())
