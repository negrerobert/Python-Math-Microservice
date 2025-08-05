"""
Custom middleware for logging and performance monitoring
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import api_logger, performance_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses with performance metrics"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())[:8]

        # Start timing
        start_time = time.time()

        # Get client info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        # Log incoming request
        api_logger.info("Request started", extra={
            'request_id': request_id,
            'method': request.method,
            'url': str(request.url),
            'path': request.url.path,
            'query_params': dict(request.query_params),
            'client_ip': client_ip,
            'user_agent': user_agent,
            'content_type': request.headers.get("content-type"),
            'content_length': request.headers.get("content-length")
        })

        # Add request ID to request state for use in routes
        request.state.request_id = request_id

        # Process request
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time

            # Log successful response
            api_logger.info("Request completed", extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'processing_time_ms': round(processing_time * 1000, 3),
                'response_size': response.headers.get("content-length", "unknown")
            })

            # Log performance metrics
            performance_logger.info("Request performance", extra={
                'request_id': request_id,
                'endpoint': request.url.path,
                'method': request.method,
                'processing_time_ms': round(processing_time * 1000, 3),
                'status_code': response.status_code,
                'client_ip': client_ip
            })

            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Processing-Time-MS"] = str(round(processing_time * 1000, 3))

            return response

        except Exception as e:
            processing_time = time.time() - start_time

            # Log failed request
            api_logger.error("Request failed", extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'processing_time_ms': round(processing_time * 1000, 3),
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)

            # Re-raise the exception to let FastAPI handle it
            raise


class CacheMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to log cache metrics for math operations"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only monitor math operation endpoints
        if not request.url.path.startswith("/api/v1/math/"):
            return await call_next(request)

        # Skip non-math operations
        operation_endpoints = ["/power", "/fibonacci", "/factorial"]
        if not any(endpoint in request.url.path for endpoint in operation_endpoints):
            return await call_next(request)

        # Import here to avoid circular imports
        from app.utils.cache import math_cache

        # Get cache stats before request
        stats_before = math_cache.get_stats()

        # Process request
        response = await call_next(request)

        # Get cache stats after request
        stats_after = math_cache.get_stats()

        # Log cache metrics if there was a change
        if stats_after['hits'] != stats_before['hits'] or stats_after['misses'] != stats_before['misses']:
            cache_action = "hit" if stats_after['hits'] > stats_before['hits'] else "miss"

            from app.utils.logger import cache_logger
            cache_logger.info("Cache metrics", extra={
                'request_id': getattr(request.state, 'request_id', 'unknown'),
                'endpoint': request.url.path,
                'cache_action': cache_action,
                'total_hits': stats_after['hits'],
                'total_misses': stats_after['misses'],
                'hit_rate_percent': stats_after['hit_rate_percent'],
                'cache_size': stats_after['current_size']
            })

        return response