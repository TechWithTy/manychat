"""
ManyChat Facebook Page API Client.

This module provides an interface to interact with the ManyChat Facebook Page API,
specifically for retrieving page information.
"""

from app.core.third_party_integrations.manychat.api._requests import (
    BaseRequest,
)
from app.core.third_party_integrations.manychat.api.facebook._responses import (
    PageInfoResponse,
)
from app.core.third_party_integrations.manychat.client import ManyChatClient


class GetPageInfoRequest(BaseRequest):
    """
    Request model for getting page information.
    
    This endpoint doesn't require any parameters, but we still create a request
    class for consistency and future extensibility.
    """
    pass


async def get_page_info(
    client: ManyChatClient,
) -> PageInfoResponse:
    """
    Retrieve information about the Facebook page.
    
    This endpoint returns details about the page including its name, category,
    avatar link, and other metadata.
    
    Args:
        client: An authenticated ManyChatClient instance.
        
    Returns:
        PageInfoResponse containing the page information.
        
    Raises:
        ManyChatAPIError: If the API request fails.
        ManyChatAuthError: If authentication fails.
        ManyChatRateLimitError: If rate limit is exceeded.
    """
    response = await client.request(
        method="GET",
        endpoint="fb/page/getInfo",
        response_model=PageInfoResponse
    )
    return response


# Example usage:
# async def example():
#     client = ManyChatClient(api_key="your_api_key")
#     try:
#         page_info = await get_page_info(client)
#         print(f"Page Name: {page_info.data.name}")
#         print(f"Category: {page_info.data.category}")
#         print(f"Pro Account: {page_info.data.is_pro}")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         await client.close()