"""
API routes for mathematical operations
"""
import time
import json
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import (
    PowerRequest, FibonacciRequest, FactorialRequest,
    MathResponse, ErrorResponse, ApiRequestHistory,
    OperationStatsResponse, HistoryResponse
)
from app.controllers.math_controller import MathController
from app.controllers.database_controller import DatabaseController
from app.database import get_db
from app.utils.cache import math_cache
from app.utils.logger import api_logger

# Create router instance
router = APIRouter(prefix="/api/v1/math", tags=["Mathematics"])

# Initialize controller
math_controller = MathController()


@router.post("/power", response_model=MathResponse)
async def calculate_power(request: PowerRequest, db: AsyncSession = Depends(get_db)):
    """
    Calculate base raised to the power of exponent

    Example:
        POST /api/v1/math/power
        {"base": 2, "exponent": 3}
        Returns: {"operation": "power", "input_values": {"base": 2, "exponent": 3}, "result": 8, "success": true}
    """
    start_time = time.time()
    input_data = {"base": request.base, "exponent": request.exponent}

    try:
        result = math_controller.calculate_power(request.base, request.exponent)
        execution_time_ms = (time.time() - start_time) * 1000

        # Save to database
        await DatabaseController.save_api_request(
            db=db,
            operation="power",
            input_data=input_data,
            result=result,
            success=True,
            execution_time_ms=execution_time_ms
        )

        api_logger.info("Power calculation successful", extra={
            'base': request.base,
            'exponent': request.exponent,
            'result': result,
            'execution_time_ms': round(execution_time_ms, 3)
        })

        return MathResponse(
            operation="power",
            input_values=input_data,
            result=result
        )
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000

        # Save failed request to database
        await DatabaseController.save_api_request(
            db=db,
            operation="power",
            input_data=input_data,
            success=False,
            error_message=str(e),
            execution_time_ms=execution_time_ms
        )

        # Re-raise to let exception handlers deal with it
        raise


@router.post("/fibonacci", response_model=MathResponse)
async def calculate_fibonacci(request: FibonacciRequest, db: AsyncSession = Depends(get_db)):
    """
    Calculate the nth Fibonacci number

    Example:
        POST /api/v1/math/fibonacci
        {"n": 10}
        Returns: {"operation": "fibonacci", "input_values": {"n": 10}, "result": 55, "success": true}
    """
    start_time = time.time()
    input_data = {"n": request.n}

    try:
        result = math_controller.calculate_fibonacci(request.n)
        execution_time_ms = (time.time() - start_time) * 1000

        # Save to database
        await DatabaseController.save_api_request(
            db=db,
            operation="fibonacci",
            input_data=input_data,
            result=result,
            success=True,
            execution_time_ms=execution_time_ms
        )

        api_logger.info("Fibonacci calculation successful", extra={
            'n': request.n,
            'result': result,
            'execution_time_ms': round(execution_time_ms, 3)
        })

        return MathResponse(
            operation="fibonacci",
            input_values=input_data,
            result=result
        )
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000

        # Save failed request to database
        await DatabaseController.save_api_request(
            db=db,
            operation="fibonacci",
            input_data=input_data,
            success=False,
            error_message=str(e),
            execution_time_ms=execution_time_ms
        )

        # Re-raise to let exception handlers deal with it
        raise


@router.post("/factorial", response_model=MathResponse)
async def calculate_factorial(request: FactorialRequest, db: AsyncSession = Depends(get_db)):
    """
    Calculate factorial of n

    Example:
        POST /api/v1/math/factorial
        {"n": 5}
        Returns: {"operation": "factorial", "input_values": {"n": 5}, "result": 120, "success": true}
    """
    start_time = time.time()
    input_data = {"n": request.n}

    try:
        result = math_controller.calculate_factorial(request.n)
        execution_time_ms = (time.time() - start_time) * 1000

        # Save to database
        await DatabaseController.save_api_request(
            db=db,
            operation="factorial",
            input_data=input_data,
            result=result,
            success=True,
            execution_time_ms=execution_time_ms
        )

        api_logger.info("Factorial calculation successful", extra={
            'n': request.n,
            'result': result,
            'execution_time_ms': round(execution_time_ms, 3)
        })

        return MathResponse(
            operation="factorial",
            input_values=input_data,
            result=result
        )
    except Exception as e:
        execution_time_ms = (time.time() - start_time) * 1000

        # Save failed request to database
        await DatabaseController.save_api_request(
            db=db,
            operation="factorial",
            input_data=input_data,
            success=False,
            error_message=str(e),
            execution_time_ms=execution_time_ms
        )

        # Re-raise to let exception handlers deal with it
        raise


@router.get("/history", response_model=HistoryResponse)
async def get_request_history(
    operation: Optional[str] = Query(None, description="Filter by operation type"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of records per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get API request history with pagination and filtering

    Query Parameters:
        - operation: Filter by operation type (power, fibonacci, factorial)
        - page: Page number (default: 1)
        - page_size: Records per page (default: 20, max: 100)
    """
    offset = (page - 1) * page_size

    # Get requests from database
    requests = await DatabaseController.get_api_requests(
        db=db,
        operation=operation,
        limit=page_size,
        offset=offset
    )

    # Convert to response format
    request_history = []
    for req in requests:
        request_history.append(ApiRequestHistory(
            id=req.id,
            operation=req.operation,
            input_data=req.input_data,
            result=req.result,
            success=req.success,
            error_message=req.error_message,
            timestamp=req.timestamp.isoformat(),
            execution_time_ms=req.execution_time_ms
        ))

    # For simplicity, we'll use the number of returned records
    total_records = len(request_history)

    return HistoryResponse(
        total_records=total_records,
        page=page,
        page_size=page_size,
        requests=request_history
    )


@router.get("/stats", response_model=List[OperationStatsResponse])
async def get_operation_statistics(db: AsyncSession = Depends(get_db)):
    """
    Get operation statistics

    Returns statistics for all operations including:
    - Total requests
    - Success/failure counts
    - Success rate
    - Average execution time
    """
    stats = await DatabaseController.get_operation_stats(db)

    response = []
    for stat in stats:
        success_rate = (stat.successful_requests / stat.total_requests * 100) if stat.total_requests > 0 else 0
        response.append(OperationStatsResponse(
            operation=stat.operation,
            total_requests=stat.total_requests,
            successful_requests=stat.successful_requests,
            failed_requests=stat.failed_requests,
            success_rate=round(success_rate, 2),
            avg_execution_time_ms=round(stat.avg_execution_time_ms, 3),
            last_updated=stat.last_updated.isoformat()
        ))

    return response


@router.get("/cache/stats")
async def get_cache_statistics():
    """
    Get cache performance statistics

    Returns detailed information about cache hits, misses, and performance metrics
    """
    stats = math_cache.get_stats()

    api_logger.info("Cache stats requested", extra=stats)

    return {
        "cache_statistics": stats,
        "message": "Cache is performing well" if stats['hit_rate_percent'] > 50 else "Consider cache optimization"
    }


@router.get("/cache/info")
async def get_cache_info():
    """
    Get detailed cache information including sample keys
    """
    info = math_cache.get_cache_info()

    api_logger.info("Cache info requested", extra={
        'total_keys': info['total_keys'],
        'hit_rate': info['stats']['hit_rate_percent']
    })

    return info


@router.post("/cache/clear")
async def clear_cache():
    """
    Clear all cached results

    This endpoint clears the entire cache, forcing all subsequent requests
    to perform fresh calculations.
    """
    old_stats = math_cache.get_stats()
    math_cache.clear()
    new_stats = math_cache.get_stats()

    api_logger.info("Cache cleared", extra={
        'items_removed': old_stats['current_size'],
        'cache_size_before': old_stats['current_size'],
        'cache_size_after': new_stats['current_size']
    })

    return {
        "message": "Cache cleared successfully",
        "items_removed": old_stats['current_size'],
        "cache_size": new_stats['current_size']
    }


@router.delete("/cache/{operation}")
async def clear_operation_cache(operation: str):
    """
    Clear cache for a specific operation type
    """
    if operation not in ["power", "fibonacci", "factorial"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid operation. Must be one of: power, fibonacci, factorial"
        )

    # For simplicity, we'll clear the entire cache
    old_size = len(math_cache.cache)
    math_cache.clear()

    api_logger.info("Operation cache cleared", extra={
        'operation': operation,
        'items_removed': old_size
    })

    return {
        "message": f"Cache cleared for operation: {operation}",
        "items_removed": old_size,
        "note": "Currently clears entire cache - implement selective clearing for production"
    }


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "math-microservice"}