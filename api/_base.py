"""Base models and utilities for ManyChat API interactions."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar, Union
from pydantic import BaseModel, Field

T = TypeVar('T', bound='BaseModel')


class APIError(Exception):
    """Base exception for all API-related errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 raw_response: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.raw_response = raw_response
        super().__init__(message)


class BaseRequest(BaseModel, ABC):
    """Base class for all API request models."""
    
    class Config:
        json_encoders = {
            # Add custom JSON encoders here if needed
        }
        extra = "forbid"  # Reject extra fields
        
    def to_api_format(self) -> Dict[str, Any]:
        """Convert the model to the format expected by the API."""
        return self.dict(exclude_none=True)


class BaseResponse(BaseModel, Generic[T], ABC):
    """Base class for all API response models."""
    
    class Config:
        json_encoders = {
            # Add custom JSON encoders here if needed
        }
        extra = "ignore"  # Be permissive with extra fields from API
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'BaseResponse[T]':
        """Create a response model from API response data."""
        return cls.parse_obj(data)


class PaginatedResponse(BaseResponse[T]):
    """Base class for paginated API responses."""
    data: list[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    limit: int = 10
    has_more: bool = False
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, index: int) -> T:
        return self.data[index]
    
    def __iter__(self):
        return iter(self.data)


class ErrorResponse(BaseModel):
    """Standard error response from ManyChat API."""
    status: str
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None
    
    def raise_for_status(self):
        """Raise an appropriate exception based on the error response."""
        if self.status == "error":
            raise APIError(
                message=self.message,
                status_code=self.code,
                raw_response=self.dict()
            )


class SuccessResponse(BaseResponse[T]):
    """Standard success response from ManyChat API."""
    status: str = "success"
    data: Optional[T] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'SuccessResponse[T]':
        """Create a success response from API data."""
        if data.get("status") != "success":
            raise ValueError("Not a success response")
        return cls.parse_obj(data)


class EmptyResponse(SuccessResponse[None]):
    """Response for successful operations with no return data."""
    data: None = None
