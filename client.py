"""Async ManyChat API client implementation.

This module provides an async client for interacting with the ManyChat API,
including rate limiting, retries, and error handling.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional, TypeVar, cast
from urllib.parse import urljoin

import aiohttp
import backoff
from pydantic import ValidationError

from . import __version__
from .config import ManyChatConfig, config
from .api.facebook._exceptions import (
    ManyChatAPIError,
    ManyChatRateLimitError,
    ManyChatValidationError,
    ManyChatAuthError,
)
from .api.facebook._requests import BaseRequest
from .api.facebook._responses import BaseResponse

# Type variables for generic method returns
T = TypeVar("T", bound=BaseResponse)

# Configure logger
logger = logging.getLogger(__name__)


class ManyChatClient:
    """Async client for interacting with the ManyChat API.
    
    Handles authentication, request/response serialization, rate limiting,
    retries, and error handling.
    """
    
    def __init__(self, config: Optional[ManyChatConfig] = None):
        """Initialize the ManyChat client.
        
        Args:
            config: Configuration instance. If not provided, loads from environment.
        """
        self.config = config or ManyChatConfig()
        self._session: Optional[aiohttp.ClientSession] = None
        self._rate_limit_semaphore = asyncio.Semaphore(
            self.config.rate_limit / 60  # Convert per-minute to per-second
        )
        self._last_request_time: float = 0
        
    async def __aenter__(self) -> "ManyChatClient":
        """Async context manager entry."""
        await self.start()
        return self
        
    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()
    
    async def start(self) -> None:
        """Initialize the client session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "User-Agent": f"ManyChat-Python-SDK/{__version__}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.api_key}",
                },
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                raise_for_status=True,
            )
    
    async def close(self) -> None:
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _enforce_rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        async with self._rate_limit_semaphore:
            now = asyncio.get_event_loop().time()
            elapsed = now - self._last_request_time
            if elapsed < 1.0:  # Ensure at least 1s between requests
                await asyncio.sleep(1.0 - elapsed)
            self._last_request_time = asyncio.get_event_loop().time()
    
    @backoff.on_exception(
        backoff.expo,
        (
            aiohttp.ClientError,
            asyncio.TimeoutError,
            ManyChatRateLimitError,
        ),
        max_tries=3,
        jitter=backoff.full_jitter,
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        request_data: Optional[BaseRequest] = None,
        response_model: type[T] = BaseResponse,
    ) -> T:
        """Make an authenticated request to the ManyChat API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            request_data: Request data model
            response_model: Pydantic model for response validation
            
        Returns:
            Parsed response data
            
        Raises:
            ManyChatAPIError: For API-level errors
            ManyChatAuthError: For authentication failures
            ManyChatRateLimitError: For rate limiting issues
            ManyChatValidationError: For request/response validation errors
        """
        if self._session is None or self._session.closed:
            await self.start()
        
        url = urljoin(self.config.api_url, endpoint)
        
        # Prepare request data
        json_data = request_data.dict(exclude_none=True) if request_data else None
        
        # Enforce rate limiting
        await self._enforce_rate_limit()
        
        try:
            logger.debug(
                "Making %s request to %s with data: %s",
                method,
                url,
                json_data,
            )
            
            async with self._session.request(
                method=method,
                url=url,
                json=json_data,
            ) as response:
                response_data = await response.json()
                
                logger.debug(
                    "Received response from %s %s: %s",
                    method,
                    url,
                    response_data,
                )
                
                # Handle API errors
                if response.status >= 400:
                    if response.status == 401:
                        raise ManyChatAuthError("Invalid API key")
                    if response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        raise ManyChatRateLimitError(
                            f"Rate limit exceeded. Retry after {retry_after} seconds",
                            retry_after=retry_after,
                        )
                    raise ManyChatAPIError(
                        f"API request failed with status {response.status}: {response_data}",
                        status_code=response.status,
                        response=response_data,
                    )
                
                # Validate and parse response
                try:
                    return response_model.parse_obj(response_data)
                except ValidationError as e:
                    raise ManyChatValidationError(
                        f"Failed to validate response: {e}"
                    ) from e
                    
        except aiohttp.ClientError as e:
            logger.error("Request failed: %s", str(e))
            raise ManyChatAPIError(f"Request failed: {str(e)}") from e
        except asyncio.TimeoutError as e:
            logger.error("Request timed out")
            raise ManyChatAPIError("Request timed out") from e
    
    # Public API methods will be added here
    # Example:
    # async def get_subscriber_info(self, subscriber_id: str) -> SubscriberInfoResponse:
    #     """Get subscriber information."""
    #     request = GetSubscriberInfoRequest(subscriber_id=subscriber_id)
    #     return await self._request(
    #         "POST",
    #         "/subscriber/getInfo",
    #         request_data=request,
    #         response_model=SubscriberInfoResponse,
    #     )


# Singleton instance for easy import
client = ManyChatClient()

__all__ = ["ManyChatClient", "client"]
