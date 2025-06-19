"""Exceptions for the ManyChat API client."""
from typing import Any, Dict, Optional


class ManyChatError(Exception):
    """Base exception for all ManyChat API errors."""
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ):
        self.status_code = status_code
        self.response = response
        self.request_id = request_id
        super().__init__(message)


class ManyChatAPIError(ManyChatError):
    """Raised when the ManyChat API returns an error response."""
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(
            f"API request failed: {message}", status_code, response, request_id
        )


class ManyChatAuthError(ManyChatError):
    """Raised when authentication fails or access is denied."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class ManyChatRateLimitError(ManyChatError):
    """Raised when the rate limit is exceeded."""
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
    ):
        self.retry_after = retry_after
        if retry_after:
            message = f"{message}. Retry after {retry_after} seconds"
        super().__init__(message, status_code=429)


class ManyChatValidationError(ManyChatError):
    """Raised when request validation fails."""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400)


class ManyChatNotFoundError(ManyChatError):
    """Raised when a requested resource is not found."""
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class ManyChatConflictError(ManyChatError):
    """Raised when there's a conflict with the current state."""
    def __init__(self, message: str = "Conflict with current state"):
        super().__init__(message, status_code=409)


class ManyChatServerError(ManyChatError):
    """Raised when the ManyChat server encounters an error."""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, status_code=500)


class ManyChatTimeoutError(ManyChatError):
    """Raised when a request times out."""
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message)


class ManyChatConnectionError(ManyChatError):
    """Raised when there are connection issues."""
    def __init__(self, message: str = "Connection error"):
        super().__init__(message)


class ManyChatRetryError(ManyChatError):
    """Raised when a request should be retried."""
    def __init__(self, message: str = "Request should be retried"):
        super().__init__(message)