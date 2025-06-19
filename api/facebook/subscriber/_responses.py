from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, HttpUrl

from app.core.third_party_integrations.manychat.api._responses import SuccessResponse


class UserRef(BaseModel):
    """Model for user reference data."""
    user_ref: str = Field(..., description="User reference ID")
    opted_in: datetime = Field(..., description="When the user opted in")


class CustomField(BaseModel):
    """Model for custom field data."""
    id: int = Field(..., description="Field ID")
    name: str = Field(..., description="Field name")
    type: str = Field(..., description="Field type (text, number, etc.)")
    description: Optional[str] = Field(None, description="Field description")
    value: Union[str, int, bool, datetime, None] = Field(
        None,
        description="Field value (can be string, number, boolean, or datetime)"
    )


class Tag(BaseModel):
    """Model for tag data."""
    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")


class SubscriberInfo(BaseModel):
    """Model for subscriber information."""
    id: str = Field(..., description="Subscriber ID")
    page_id: str = Field(..., description="Page ID")
    user_refs: List[UserRef] = Field(
        default_factory=list,
        description="List of user references"
    )
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    name: Optional[str] = Field(None, description="Full name")
    gender: Optional[str] = Field(None, description="Gender")
    profile_pic: Optional[HttpUrl] = Field(None, description="Profile picture URL")
    locale: Optional[str] = Field(None, description="Locale")
    language: Optional[str] = Field(None, description="Language")
    timezone: Optional[str] = Field(None, description="Timezone")
    live_chat_url: Optional[str] = Field(None, description="Live chat URL")
    last_input_text: Optional[str] = Field(None, description="Last input text")
    optin_phone: bool = Field(False, description="If phone opt-in is enabled")
    phone: Optional[str] = Field(None, description="Phone number")
    optin_email: bool = Field(False, description="If email opt-in is enabled")
    email: Optional[str] = Field(None, description="Email address")
    subscribed: Optional[datetime] = Field(None, description="Subscription date")
    last_interaction: Optional[datetime] = Field(None, description="Last interaction")
    last_seen: Optional[datetime] = Field(None, description="Last seen online")
    is_followup_enabled: bool = Field(False, description="If follow-up is enabled")
    ig_username: Optional[str] = Field(None, description="Instagram username")
    ig_id: Optional[int] = Field(None, description="Instagram ID")
    whatsapp_phone: Optional[str] = Field(None, description="WhatsApp phone number")
    optin_whatsapp: bool = Field(False, description="If WhatsApp opt-in is enabled")
    custom_fields: List[CustomField] = Field(
        default_factory=list,
        description="List of custom fields"
    )
    tags: List[Tag] = Field(
        default_factory=list,
        description="List of tags"
    )


class GetSubscriberInfoResponse(SuccessResponse):
    """Response model for get subscriber info endpoint."""
    data: SubscriberInfo = Field(..., description="Subscriber information")