"""
Database index creation script.

This module creates all necessary MongoDB indexes for optimal query performance.

Index Strategy:
- Unique indexes: Enforce business constraints (email, slug, sku, order_number)
- Query indexes: Speed up common queries (category, price, rating)
- Compound indexes: Optimize multi-field queries (category + price)
- Text indexes: Enable full-text search (product name, description)
- TTL indexes: Automatic cleanup of expired documents (carts, tokens)
"""

from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_indexes(db: AsyncIOMotorDatabase) -> None:
    """
    Create all database indexes.

    Args:
        db: MongoDB database instance
    """

    print("📊 Creating database indexes...")

    # ===== PRODUCTS Collection =====
    await db.products.create_index("slug", unique=True)
    await db.products.create_index("sku", unique=True)
    await db.products.create_index("category_id")
    await db.products.create_index([("price", 1)])
    await db.products.create_index([("average_rating", -1)])
    await db.products.create_index([("created_at", -1)])

    # Compound index for filtering by category + price
    await db.products.create_index([("category_id", 1), ("price", 1)])

    # Text index for full-text search on name and description
    await db.products.create_index([("name", "text"), ("description", "text")])

    print("  ✅ Products indexes created")

    # ===== CATEGORIES Collection =====
    await db.categories.create_index("slug", unique=True)
    await db.categories.create_index("parent_id")
    await db.categories.create_index([("display_order", 1)])

    print("  ✅ Categories indexes created")

    # ===== USERS Collection =====
    await db.users.create_index("email", unique=True)
    await db.users.create_index([("created_at", -1)])

    print("  ✅ Users indexes created")

    # ===== CARTS Collection =====
    # Sparse unique index (only for non-null user_id)
    await db.carts.create_index("user_id", unique=True, sparse=True)
    await db.carts.create_index("session_id", unique=True, sparse=True)

    # TTL index for automatic cleanup of expired guest carts
    await db.carts.create_index("expires_at", expireAfterSeconds=0)

    print("  ✅ Carts indexes created")

    # ===== ORDERS Collection =====
    await db.orders.create_index("order_number", unique=True)
    await db.orders.create_index("user_id")
    await db.orders.create_index([("user_id", 1), ("created_at", -1)])
    await db.orders.create_index([("status", 1)])

    print("  ✅ Orders indexes created")

    # ===== PAYMENTS Collection =====
    await db.payments.create_index("transaction_id", unique=True)
    await db.payments.create_index("order_id")
    await db.payments.create_index([("status", 1)])

    print("  ✅ Payments indexes created")

    # ===== ADDRESSES Collection =====
    await db.addresses.create_index("user_id")
    await db.addresses.create_index([("user_id", 1), ("is_default", -1)])

    print("  ✅ Addresses indexes created")

    # ===== REVIEWS Collection =====
    await db.reviews.create_index("product_id")
    await db.reviews.create_index("user_id")
    await db.reviews.create_index([("product_id", 1), ("created_at", -1)])

    print("  ✅ Reviews indexes created")

    # ===== REFRESH_TOKENS Collection =====
    await db.refresh_tokens.create_index("token", unique=True)
    await db.refresh_tokens.create_index("user_id")

    # TTL index for automatic cleanup of expired tokens
    await db.refresh_tokens.create_index("expires_at", expireAfterSeconds=0)

    print("  ✅ Refresh tokens indexes created")

    print("✅ All database indexes created successfully!")


if __name__ == "__main__":
    """Run this script directly to create indexes"""
    import asyncio
    from src.db.mongodb import connect_to_mongo, get_database, close_mongo_connection
    from src.core.config import settings

    async def main():
        await connect_to_mongo(settings.MONGODB_URI)
        await create_indexes(get_database())
        await close_mongo_connection()

    asyncio.run(main())
