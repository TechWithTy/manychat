"""
ManyChat Bot Fields API Client.

This module provides an interface to interact with the ManyChat Bot Fields API,
specifically for updating bot fields.
"""

from typing import Optional, Union, Any

from app.core.third_party_integrations.manychat.api.facebook._requests import (
    SetBotFieldsRequest,
    BotFieldUpdate
)
from app.core.third_party_integrations.manychat.api.facebook._responses import (
    SetBotFieldsResponse
)
from app.core.third_party_integrations.manychat.client import ManyChatClient


async def set_bot_fields(
    client: ManyChatClient,
    fields: list[dict[str, Any]]
) -> SetBotFieldsResponse:
    """
    Update multiple bot fields in a single request.
    
    Args:
        client: An authenticated ManyChatClient instance.
        fields: List of field updates. Each item should be a dict with:
               - field_id (int, optional): ID of the field to update
               - field_name (str, optional): Name of the field to update
               - field_value: Value to set for the field (str, int, bool, or float)
               Note: Either field_id or field_name must be provided for each field.
        
    Returns:
        SetBotFieldsResponse containing the results of each update operation.
        
    Raises:
        ManyChatAPIError: If the API request fails.
        ManyChatAuthError: If authentication fails.
        ManyChatRateLimitError: If rate limit is exceeded.
        ValueError: If validation of fields fails.
    """
    # Convert dicts to BotFieldUpdate models for validation
    field_updates = [BotFieldUpdate(**field) for field in fields]
    
    # Create and validate the request
    request = SetBotFieldsRequest(fields=field_updates)
    
    # Make the API call
    response = await client.request(
        method="POST",
        endpoint="fb/page/setBotFields",
        request_data=request,
        response_model=SetBotFieldsResponse
    )
    return response


async def set_bot_field(
    client: ManyChatClient,
    *,
    field_id: Optional[int] = None,
    field_name: Optional[str] = None,
    field_value: Union[str, int, bool, float]
) -> SetBotFieldsResponse:
    """
    Update a single bot field.
    
    Args:
        client: An authenticated ManyChatClient instance.
        field_id: ID of the field to update (either field_id or field_name must be provided).
        field_name: Name of the field to update (either field_id or field_name must be provided).
        field_value: Value to set for the field.
        
    Returns:
        SetBotFieldsResponse containing the result of the update operation.
        
    Raises:
        ValueError: If neither field_id nor field_name is provided.
    """
    if field_id is None and field_name is None:
        raise ValueError("Either field_id or field_name must be provided")
        
    return await set_bot_fields(
        client=client,
        fields=[{
            **({"field_id": field_id} if field_id is not None else {}),
            **({"field_name": field_name} if field_name is not None else {}),
            "field_value": field_value
        }]
    )


# Example usage:
# async def example():
#     client = ManyChatClient(api_key="your_api_key")
#     try:
#         # Update multiple fields
#         response = await set_bot_fields(
#             client,
#             fields=[
#                 {"field_id": 77777777, "field_value": 555},
#                 {"field_name": "count", "field_value": 12}
#             ]
#         )
#         print(f"Updated {sum(1 for r in response.data if r.success)} fields successfully")
#         
#         # Update a single field by name
#         response = await set_bot_field(
#             client,
#             field_name="welcome_message",
#             field_value="Hello, welcome to our service!"
#         )
#     finally:
#         await client.close()