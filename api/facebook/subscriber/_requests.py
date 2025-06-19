from pydantic import Field

from app.core.third_party_integrations.manychat.api._requests import BaseRequest


# In _requests.py
class AddTagByNameRequest(BaseRequest):
    """Request model for adding a tag to a subscriber by name."""
    subscriber_id: str = Field(
        ...,
        alias="subscriber_id",
        description="The subscriber's ID"
    )
    tag_name: str = Field(
        ...,
        alias="tag_name",
        description="Name of the tag to add to the subscriber"
    )
    

class GetSubscriberInfoRequest(BaseRequest):
    """Request model for getting subscriber information."""
    subscriber_id: str = Field(
        ...,
        alias="subscriber_id",
        description="The subscriber's ID"
    )
    fields: list[str] | None = Field(
        None,
        description="Optional list of fields to include in the response"
    )