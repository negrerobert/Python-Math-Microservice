"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Union, List


class PowerRequest(BaseModel):
    """Request model for power operation"""
    base: Union[int, float] = Field(..., description="Base number")
    exponent: Union[int, float] = Field(..., description="Exponent")


class FibonacciRequest(BaseModel):
    """Request model for fibonacci operation"""
    n: int = Field(..., ge=0, description="Position in fibonacci sequence (non-negative)")


class FactorialRequest(BaseModel):
    """Request model for factorial operation"""
    n: int = Field(..., ge=0, description="Number to calculate factorial (non-negative)")


class MathResponse(BaseModel):
    """Response model for all math operations"""
    operation: str = Field(..., description="Type of operation performed")
    input_values: dict = Field(..., description="Input parameters used")
    result: Union[int, float] = Field(..., description="Calculation result")
    success: bool = Field(default=True, description="Whether operation was successful")


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error message")
    operation: str = Field(..., description="Operation that failed")
    success: bool = Field(default=False, description="Always false for errors")


class ApiRequestHistory(BaseModel):
    """Response model for API request history"""
    id: int
    operation: str
    input_data: str  # JSON string
    result: Union[float, None]
    success: bool
    error_message: Union[str, None]
    timestamp: str  # ISO format datetime string
    execution_time_ms: Union[float, None]

    class Config:
        from_attributes = True  # Allows creation from SQLAlchemy models


class OperationStatsResponse(BaseModel):
    """Response model for operation statistics"""
    operation: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    avg_execution_time_ms: float
    last_updated: str

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    """Response model for history endpoint"""
    total_records: int
    page: int
    page_size: int
    requests: List[ApiRequestHistory]