"""
Custom exceptions and exception handlers
"""
from typing import Dict, Any, Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.utils.logger import app_logger


class MathOperationError(Exception):
    """Custom exception for mathematical operation errors"""

    def __init__(self, operation: str, message: str, input_data: Dict[str, Any] = None):
        self.operation = operation
        self.message = message
        self.input_data = input_data or {}
        super().__init__(self.message)


class CacheError(Exception):
    """Custom exception for cache-related errors"""

    def __init__(self, message: str, operation: str = None):
        self.message = message
        self.operation = operation
        super().__init__(self.message)


async def math_operation_exception_handler(request: Request, exc: MathOperationError) -> JSONResponse:
    """Handle mathematical operation errors"""
    app_logger.error("Math operation error", extra={
        'operation': exc.operation,
        'error': exc.message,
        'input_data': exc.input_data,
        'path': str(request.url),
        'method': request.method
    })

    return JSONResponse(
        status_code=400,
        content={
            "error": exc.message,
            "operation": exc.operation,
            "success": False,
            "error_type": "MathOperationError",
            "input_data": exc.input_data
        }
    )


async def cache_exception_handler(request: Request, exc: CacheError) -> JSONResponse:
    """Handle cache-related errors"""
    app_logger.warning("Cache error", extra={
        'error': exc.message,
        'operation': exc.operation,
        'path': str(request.url),
        'method': request.method
    })

    return JSONResponse(
        status_code=500,
        content={
            "error": "Cache system error - operation continued without caching",
            "success": False,
            "error_type": "CacheError"
        }
    )


async def validation_exception_handler(request: Request, exc: Union[ValidationError, RequestValidationError]) -> JSONResponse:
    """Handle Pydantic validation errors with detailed messages"""
    errors = []

    # Handle both ValidationError and RequestValidationError
    if hasattr(exc, 'errors'):
        error_details = exc.errors()
    else:
        error_details = []

    for error in error_details:
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        errors.append({
            "field": field,
            "message": error.get("msg", "Validation error"),
            "invalid_value": error.get("input", "N/A"),
            "error_type": error.get("type", "validation_error")
        })

    app_logger.warning("Validation error", extra={
        'errors': errors,
        'path': str(request.url),
        'method': request.method,
        'error_count': len(errors),
        'exception_type': type(exc).__name__
    })

    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid input data",
            "success": False,
            "error_type": "ValidationError",
            "details": errors,  # This is what the test script looks for
            "error_count": len(errors)
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with logging"""
    app_logger.error("HTTP exception", extra={
        'status_code': exc.status_code,
        'detail': exc.detail,
        'path': str(request.url),
        'method': request.method
    })

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "success": False,
            "error_type": "HTTPException",
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    app_logger.critical("Unexpected error", extra={
        'error': str(exc),
        'error_type': type(exc).__name__,
        'path': str(request.url),
        'method': request.method
    }, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "success": False,
            "error_type": "InternalServerError"
        }
    )