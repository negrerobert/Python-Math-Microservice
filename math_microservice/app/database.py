"""
Database configuration and connection management
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.database_models import Base
from app.utils.logger import db_logger

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./math_microservice.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Disabled verbose SQL logging - using structured logging instead
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Dependency to get database session
    Use this in FastAPI route dependencies
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Database utility functions
class DatabaseManager:
    """Database operations manager"""

    @staticmethod
    async def init_database():
        """Initialize database and create tables"""
        try:
            await create_tables()
            db_logger.info("Database initialized successfully")
        except Exception as e:
            db_logger.error("Database initialization failed", extra={'error': str(e)}, exc_info=True)
            raise

    @staticmethod
    async def close_database():
        """Close database connections"""
        try:
            await engine.dispose()
            db_logger.info("Database connections closed successfully")
        except Exception as e:
            db_logger.error("Error closing database connections", extra={'error': str(e)}, exc_info=True)