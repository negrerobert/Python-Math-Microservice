"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class ApiRequest(Base):
    """
    Model to store all API requests and responses
    """
    __tablename__ = "api_requests"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String(50), nullable=False, index=True)
    input_data = Column(Text, nullable=False)  # JSON string of input parameters
    result = Column(Float, nullable=True)  # Calculation result
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)  # Error message if operation failed
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    execution_time_ms = Column(Float, nullable=True)  # Time taken to execute operation

    def __repr__(self):
        return f"<ApiRequest(id={self.id}, operation={self.operation}, success={self.success})>"


class OperationStats(Base):
    """
    Model to store operation statistics (optional - for monitoring)
    """
    __tablename__ = "operation_stats"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String(50), nullable=False, unique=True, index=True)
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    avg_execution_time_ms = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<OperationStats(operation={self.operation}, total={self.total_requests})>"