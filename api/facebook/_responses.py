
from typing import Optional

from pydantic import BaseModel, Field

from app.core.third_party_integrations.manychat.api._responses import (
    SuccessResponse,
)
from app.core.third_party_integrations.manychat.api._enums import HttpUrl


# In _responses.py
class PageInfo(BaseModel):
    """Model representing page information in ManyChat."""
    id: int = Field(..., description="Page ID")
    name: str = Field(..., description="Page name")
    category: str = Field(..., description="Page category")
    avatar_link: Optional[HttpUrl] = Field(None, description="URL to page avatar")
    username: Optional[str] = Field(None, description="Page username")
    about: Optional[str] = Field(None, description="Page about information")
    description: Optional[str] = Field(None, description="Page description")
    is_pro: bool = Field(False, description="Whether the page is a pro account")
    timezone: str = Field(..., description="Page timezone")

class PageInfoResponse(SuccessResponse):
    """Response model for page information endpoint."""
    data: PageInfo = Field(..., description="Page information data")
    
# In _responses.py
class TagInfo(BaseModel):
    """Model representing a tag in ManyChat."""
    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")

class TagsListResponse(SuccessResponse):
    """Response model for tags list endpoint."""
    data: list[TagInfo] = Field(..., description="List of tags")
    
# In _responses.py
class BotFieldUpdateResult(BaseModel):
    """Result of a single field update operation."""
    field_id: Optional[int] = Field(None, description="ID of the updated field")
    field_name: Optional[str] = Field(None, description="Name of the updated field")
    success: bool = Field(..., description="Whether the update was successful")
    error: Optional[str] = Field(None, description="Error message if update failed")

class SetBotFieldsResponse(SuccessResponse):
    """Response model for setBotFields endpoint."""
    data: list[BotFieldUpdateResult] = Field(
        ...,
        description="Results of each field update operation"
    )