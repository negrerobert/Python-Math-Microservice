"""
Database operations controller
"""
import json
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from app.models.database_models import ApiRequest, OperationStats
from datetime import datetime


class DatabaseController:
    """Controller for database operations"""

    @staticmethod
    async def save_api_request(
            db: AsyncSession,
            operation: str,
            input_data: dict,
            result: Optional[float] = None,
            success: bool = True,
            error_message: Optional[str] = None,
            execution_time_ms: Optional[float] = None
    ) -> ApiRequest:
        """
        Save an API request to the database

        Args:
            db: Database session
            operation: Type of operation (power, fibonacci, factorial)
            input_data: Input parameters as dictionary
            result: Calculation result
            success: Whether operation was successful
            error_message: Error message if failed
            execution_time_ms: Time taken to execute

        Returns:
            Created ApiRequest record
        """
        api_request = ApiRequest(
            operation=operation,
            input_data=json.dumps(input_data),
            result=result,
            success=success,
            error_message=error_message,
            execution_time_ms=execution_time_ms
        )

        db.add(api_request)
        await db.commit()
        await db.refresh(api_request)

        # Update operation statistics
        await DatabaseController._update_operation_stats(
            db, operation, success, execution_time_ms or 0.0
        )

        return api_request

    @staticmethod
    async def get_api_requests(
            db: AsyncSession,
            operation: Optional[str] = None,
            limit: int = 100,
            offset: int = 0
    ) -> List[ApiRequest]:
        """
        Get API requests from database

        Args:
            db: Database session
            operation: Filter by operation type (optional)
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of ApiRequest records
        """
        query = select(ApiRequest).order_by(desc(ApiRequest.timestamp))

        if operation:
            query = query.where(ApiRequest.operation == operation)

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_operation_stats(db: AsyncSession) -> List[OperationStats]:
        """Get operation statistics"""
        result = await db.execute(select(OperationStats))
        return result.scalars().all()

    @staticmethod
    async def _update_operation_stats(
            db: AsyncSession,
            operation: str,
            success: bool,
            execution_time_ms: float
    ):
        """Update operation statistics (internal method)"""
        # Check if stats record exists
        result = await db.execute(
            select(OperationStats).where(OperationStats.operation == operation)
        )
        stats = result.scalar_one_or_none()

        if not stats:
            # Create new stats record
            stats = OperationStats(
                operation=operation,
                total_requests=1,
                successful_requests=1 if success else 0,
                failed_requests=0 if success else 1,
                avg_execution_time_ms=execution_time_ms
            )
            db.add(stats)
        else:
            # Update existing stats
            stats.total_requests += 1
            if success:
                stats.successful_requests += 1
            else:
                stats.failed_requests += 1

            # Update average execution time
            if stats.total_requests > 1:
                current_total_time = stats.avg_execution_time_ms * (stats.total_requests - 1)
                stats.avg_execution_time_ms = (current_total_time + execution_time_ms) / stats.total_requests
            else:
                stats.avg_execution_time_ms = execution_time_ms

        await db.commit()