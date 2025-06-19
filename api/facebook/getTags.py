"""
ManyChat Tags API Client.

This module provides an interface to interact with the ManyChat Tags API,
specifically for retrieving available tags.
"""

from typing import List, Optional

from app.core.third_party_integrations.manychat.api.facebook._base import BaseRequest
from app.core.third_party_integrations.manychat.api.facebook._responses import TagsListResponse
from app.core.third_party_integrations.manychat.client import ManyChatClient


class GetTagsRequest(BaseRequest):
    """
    Request model for getting tags.
    
    This endpoint doesn't require any parameters, but we still create a request
    class for consistency and future extensibility.
    """
    pass


async def get_tags(
    client: ManyChatClient,
) -> TagsListResponse:
    """
    Retrieve all available tags for the page.
    
    This endpoint returns a list of all tags that have been created in the page.
    
    Args:
        client: An authenticated ManyChatClient instance.
        
    Returns:
        TagsListResponse containing the list of tags.
        
    Raises:
        ManyChatAPIError: If the API request fails.
        ManyChatAuthError: If authentication fails.
        ManyChatRateLimitError: If rate limit is exceeded.
    """
    response = await client.request(
        method="GET",
        endpoint="fb/page/getTags",
        response_model=TagsListResponse
    )
    return response


async def find_tag_by_name(
    client: ManyChatClient,
    tag_name: str
) -> Optional[dict]:
    """
    Find a tag by its name (case-insensitive).
    
    Args:
        client: An authenticated ManyChatClient instance.
        tag_name: The name of the tag to find.
        
    Returns:
        The tag info if found, None otherwise.
    """
    response = await get_tags(client)
    if response.data:
        return next(
            (tag.dict() for tag in response.data if tag.name.lower() == tag_name.lower()),
            None
        )
    return None


# Example usage:
# async def example():
#     client = ManyChatClient(api_key="your_api_key")
#     try:
#         # Get all tags
#         tags_response = await get_tags(client)
#         print(f"Found {len(tags_response.data)} tags")
#         for tag in tags_response.data:
#             print(f"Tag: {tag.name} (ID: {tag.id})")
#             
#         # Find a specific tag
#         tag = await find_tag_by_name(client, "VIP")
#         if tag:
#             print(f"Found VIP tag with ID: {tag['id']}")
#     finally:
#         await client.close()