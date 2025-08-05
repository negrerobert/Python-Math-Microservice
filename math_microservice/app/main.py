"""
Main FastAPI application with logging, caching and error handling
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import ValidationError

from app.routes.math_routes import router as math_router
from app.database import DatabaseManager

# Import middleware and exception handlers
from app.utils.middleware import RequestLoggingMiddleware, CacheMetricsMiddleware
from app.utils.exceptions import (
    MathOperationError, CacheError,
    math_operation_exception_handler, cache_exception_handler,
    validation_exception_handler, http_exception_handler, general_exception_handler
)
from app.utils.logger import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI app
    Handles startup and shutdown events
    """
    # Startup
    app_logger.info("Starting Math Microservice...")
    await DatabaseManager.init_database()
    app_logger.info("Database initialized successfully")

    # Initialize cache
    from app.utils.cache import math_cache
    app_logger.info("Cache initialized", extra=math_cache.get_stats())

    yield

    # Shutdown
    app_logger.info("Shutting down Math Microservice...")
    await DatabaseManager.close_database()
    app_logger.info("Math Microservice shutdown complete")


# Create FastAPI instance
app = FastAPI(
    title="Math Microservice API",
    description="A microservice for mathematical operations with caching, logging and monitoring",
    version="3.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # Alternative documentation at /redoc
    lifespan=lifespan
)

# Add exception handlers (order matters - more specific first)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(MathOperationError, math_operation_exception_handler)
app.add_exception_handler(CacheError, cache_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add FastAPI's RequestValidationError handler
from fastapi.exceptions import RequestValidationError
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Add middleware (order matters - last added is executed first)
app.add_middleware(CacheMetricsMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Add CORS middleware (allows requests from different origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(math_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    from app.utils.cache import math_cache
    cache_stats = math_cache.get_stats()

    return {
        "message": "Welcome to Math Microservice API",
        "version": "3.0.0",
        "features": [
            "mathematical operations",
            "request persistence",
            "operation statistics",
            "in-memory caching",
            "structured logging",
            "performance monitoring"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/api/v1/math/health",
            "history": "/api/v1/math/history",
            "stats": "/api/v1/math/stats",
            "cache_stats": "/api/v1/math/cache/stats",
            "cache_info": "/api/v1/math/cache/info"
        },
        "cache_performance": {
            "hit_rate_percent": cache_stats['hit_rate_percent'],
            "cache_size": cache_stats['current_size'],
            "total_requests": cache_stats['hits'] + cache_stats['misses']
        }
    }


# This allows running with: python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)