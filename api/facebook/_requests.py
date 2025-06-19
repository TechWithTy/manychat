# In _requests.py
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator
from app.core.third_party_integrations.manychat.api._requests import BaseRequest


class BotFieldUpdate(BaseModel):
    """Model for updating a single bot field."""
    field_id: Optional[int] = Field(
        None,
        description="ID of the field to update (either field_id or field_name must be provided)"
    )
    field_name: Optional[str] = Field(
        None,
        description="Name of the field to update (either field_id or field_name must be provided)"
    )
    field_value: Union[str, int, bool, float] = Field(
        ...,
        description="Value to set for the field"
    )

    @validator('field_name', always=True)
    def validate_field_identifier(cls, v, values):
        if not v and not values.get('field_id'):
            raise ValueError("Either field_id or field_name must be provided")
        return v

class SetBotFieldsRequest(BaseRequest):
    """Request model for setting multiple bot fields."""
    fields: List[BotFieldUpdate] = Field(
        ...,
        max_items=20,
        description="List of fields to update (max 20 per request)"
    )