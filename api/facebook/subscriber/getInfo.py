"""
ManyChat Subscriber API Client.

This module provides functionality to retrieve subscriber information
from the ManyChat API.
"""

from typing import Any, Dict, List, Optional, Type

from app.core.third_party_integrations.manychat.api.facebook.subscriber._requests import (
    GetSubscriberInfoRequest,
)
from app.core.third_party_integrations.manychat.api.facebook.subscriber._responses import (
    GetSubscriberInfoResponse,
)
from app.core.third_party_integrations.manychat.client import ManyChatClient


async def get_subscriber_info(
    client: ManyChatClient,
    *,
    subscriber_id: str,
    fields: Optional[List[str]] = None
) -> GetSubscriberInfoResponse:
    """
    Get detailed information about a subscriber.

    Args:
        client: An authenticated ManyChatClient instance.
        subscriber_id: The ID of the subscriber to retrieve.
        fields: Optional list of specific fields to include in the response.

    Returns:
        GetSubscriberInfoResponse containing the subscriber's information.

    Raises:
        ManyChatAPIError: If the API request fails.
        ManyChatAuthError: If authentication fails.
        ManyChatRateLimitError: If rate limit is exceeded.
        ManyChatNotFoundError: If the subscriber is not found.
    """
    # Create and validate the request
    request = GetSubscriberInfoRequest(
        subscriber_id=subscriber_id,
        fields=fields
    )
    
    # Make the API call
    response = await client.request(
        method="GET",
        endpoint="fb/subscriber/getInfo",
        params=request.dict(exclude_none=True, by_alias=True),
        response_model=GetSubscriberInfoResponse
    )
    return response


# Example usage:
# async def example():
#     client = ManyChatClient(api_key="your_api_key")
#     try:
#         # Get subscriber info
#         response = await get_subscriber_info(
#             client,
#             subscriber_id="1234567890",
#             fields=["first_name", "last_name", "email"]
#         )
#         subscriber = response.data
#         print(f"Subscriber: {subscriber.first_name} {subscriber.last_name}")
#         print(f"Email: {subscriber.email}")
#         print(f"Tags: {[tag.name for tag in subscriber.tags]}")
#     finally:
#         await client.close()ss