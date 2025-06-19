"""
ManyChat Subscriber Tags API Client.

This module provides functionality to add tags to subscribers by tag name
in the ManyChat API.
"""

from app.core.third_party_integrations.manychat.api.facebook._responses import (
    SuccessResponse,
)
from app.core.third_party_integrations.manychat.api.facebook.subscriber._requests import (
    AddTagByNameRequest,
)
from app.core.third_party_integrations.manychat.client import ManyChatClient


async def add_tag_by_name(
    client: ManyChatClient,
    *,
    subscriber_id: str,
    tag_name: str
) -> SuccessResponse:
    """
    Add a tag to a subscriber by tag name.

    Args:
        client: An authenticated ManyChatClient instance.
        subscriber_id: The ID of the subscriber to tag.
        tag_name: The name of the tag to add.

    Returns:
        SuccessResponse indicating the result of the operation.

    Raises:
        ManyChatAPIError: If the API request fails.
        ManyChatAuthError: If authentication fails.
        ManyChatRateLimitError: If rate limit is exceeded.
        ManyChatValidationError: If input validation fails.
    """
    # Create and validate the request
    request = AddTagByNameRequest(
        subscriber_id=subscriber_id,
        tag_name=tag_name
    )
    
    # Make the API call
    response = await client.request(
        method="POST",
        endpoint="fb/subscriber/addTagByName",
        request_data=request,
        response_model=SuccessResponse
    )
    return response


# Example usage:
# async def example():
#     client = ManyChatClient(api_key="your_api_key")
#     try:
#         # Add a tag to a subscriber
#         response = await add_tag_by_name(
#             client,
#             subscriber_id="1234567890",
#             tag_name="VIP"
#         )
#         if response.status == "success":
#             print("Tag added successfully")
#         else:
#             print("Failed to add tag")
#     finally:
#         await client.close()