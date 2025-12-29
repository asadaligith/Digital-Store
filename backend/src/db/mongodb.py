"""
MongoDB client setup with Motor async driver and connection pooling.

This module provides asynchronous MongoDB connection management using Motor,
the official MongoDB async driver for Python.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

# Global database client and database instances
client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo(mongodb_uri: str, database_name: str = "ecommerce") -> None:
    """
    Connect to MongoDB with connection pooling configuration.

    Args:
        mongodb_uri: MongoDB connection string
        database_name: Name of the database to use

    Connection Pooling:
        - max_pool_size: 50 (maximum number of connections)
        - min_pool_size: 10 (minimum number of connections to maintain)
        - maxIdleTimeMS: 45000 (45 seconds - close idle connections)
        - serverSelectionTimeoutMS: 5000 (5 seconds - timeout for server selection)
    """
    global client, database

    client = AsyncIOMotorClient(
        mongodb_uri,
        maxPoolSize=50,  # Maximum concurrent connections
        minPoolSize=10,  # Keep minimum connections alive
        maxIdleTimeMS=45000,  # Close idle connections after 45 seconds
        serverSelectionTimeoutMS=5000,  # 5 second timeout for server selection
    )

    database = client[database_name]

    # Test the connection
    await database.command("ping")
    print(f"✅ Connected to MongoDB database: {database_name}")


async def close_mongo_connection() -> None:
    """
    Close MongoDB connection and cleanup resources.

    This should be called during application shutdown.
    """
    global client

    if client:
        client.close()
        print("🔌 MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get the current database instance.

    Returns:
        AsyncIOMotorDatabase instance

    Raises:
        RuntimeError: If database connection is not initialized
    """
    if database is None:
        raise RuntimeError(
            "Database connection not initialized. "
            "Call connect_to_mongo() first during application startup."
        )
    return database
