"""
Response models for ManyChat API.

This module contains Pydantic models that represent the structure of responses
returned by the ManyChat API endpoints.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, HttpUrl, validator

from app.core.third_party_integrations.manychat.api._base import (
    BaseResponse,
    ErrorResponse,
    PaginatedResponse,
    SuccessResponse,
)

# Type variable for generic response models
T = TypeVar('T')

class SubscriberStatus(str, Enum):
    """Possible status values for a subscriber."""
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    PENDING = "pending"

class SubscriberGender(str, Enum):
    """Possible gender values for a subscriber."""
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class SubscriberSource(str, Enum):
    """Possible sources for a subscriber."""
    FACEBOOK = "facebook"
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    WEB_CHAT = "web_chat"
    CUSTOM = "custom"

class FieldType(str, Enum):
    """Possible field types in ManyChat."""
    TEXT = "Text"
    NUMBER = "Number"
    DATE = "Date"
    DATETIME = "DateTime"
    BOOLEAN = "Boolean"
    URL = "URL"
    EMAIL = "Email"
    PHONE = "Phone"
    COUNTRY = "Country"
    STATE = "State"
    CITY = "City"
    ZIP = "ZIP"
    CURRENCY = "Currency"

class SubscriberField(BaseModel):
    """Model for a single custom field value for a subscriber."""
    id: str = Field(..., description="Unique identifier for the field")
    name: str = Field(..., description="Name of the field")
    type: FieldType = Field(..., description="Type of the field")
    value: Optional[Any] = Field(None, description="Value of the field")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Tag(BaseModel):
    """Model for a tag in ManyChat."""
    id: str = Field(..., description="Unique identifier for the tag")
    name: str = Field(..., description="Name of the tag")
    description: Optional[str] = Field(None, description="Description of the tag")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Subscriber(BaseModel):
    """Model representing a subscriber in ManyChat."""
    id: str = Field(..., description="Unique identifier for the subscriber")
    status: SubscriberStatus = Field(..., description="Subscription status")
    first_name: Optional[str] = Field(None, description="First name of the subscriber")
    last_name: Optional[str] = Field(None, description="Last name of the subscriber")
    name: Optional[str] = Field(None, description="Full name of the subscriber")
    gender: Optional[SubscriberGender] = Field(None, description="Gender of the subscriber")
    profile_pic: Optional[HttpUrl] = Field(None, description="URL to the subscriber's profile picture")
    locale: Optional[str] = Field(None, description="Locale of the subscriber")
    language: Optional[str] = Field(None, description="Language preference")
    timezone: Optional[int] = Field(None, description="Timezone offset in seconds")
    last_input_text: Optional[str] = Field(None, description="Last input text from the subscriber")
    last_interaction: Optional[datetime] = Field(None, description="Timestamp of last interaction")
    last_seen: Optional[datetime] = Field(None, description="When the subscriber was last seen online")
    subscribed: bool = Field(False, description="Whether the subscriber is currently subscribed")
    user_phone: Optional[str] = Field(None, description="User's phone number")
    whatsapp_phone: Optional[str] = Field(None, description="WhatsApp phone number")
    phone_number: Optional[str] = Field(None, description="Primary phone number")
    email: Optional[str] = Field(None, description="Email address")
    tags: List[Tag] = Field(default_factory=list, description="List of tags associated with the subscriber")
    custom_fields: List[SubscriberField] = Field(
        default_factory=list,
        description="List of custom field values for the subscriber"
    )
    created_at: datetime = Field(..., description="When the subscriber was created")
    updated_at: Optional[datetime] = Field(None, description="When the subscriber was last updated")

    # Validator to handle empty profile pic URLs
    @validator('profile_pic', pre=True)
    def validate_profile_pic(cls, v):
        if v == "":
            return None
        return v

# Response models for different API endpoints
class SubscriberResponse(SuccessResponse):
    """Response model for subscriber-related endpoints."""
    data: Subscriber = Field(..., description="Subscriber data")

class SubscribersResponse(PaginatedResponse):
    """Response model for paginated list of subscribers."""
    data: List[Subscriber] = Field(..., description="List of subscribers")

class TagResponse(SuccessResponse):
    """Response model for tag-related endpoints."""
    data: Tag = Field(..., description="Tag data")

class TagsResponse(PaginatedResponse):
    """Response model for paginated list of tags."""
    data: List[Tag] = Field(..., description="List of tags")

class CustomField(BaseModel):
    """Model for a custom field definition in ManyChat."""
    id: str = Field(..., description="Unique identifier for the field")
    name: str = Field(..., description="Name of the field")
    type: FieldType = Field(..., description="Type of the field")
    description: Optional[str] = Field(None, description="Description of the field")
    created_at: datetime = Field(..., description="When the field was created")
    updated_at: Optional[datetime] = Field(None, description="When the field was last updated")

class CustomFieldsResponse(PaginatedResponse):
    """Response model for paginated list of custom fields."""
    data: List[CustomField] = Field(..., description="List of custom fields")

class CustomFieldResponse(SuccessResponse):
    """Response model for a single custom field."""
    data: CustomField = Field(..., description="Custom field data")

class FlowResponse(SuccessResponse):
    """Response model for flow execution."""
    data: Dict[str, Any] = Field(..., description="Flow execution result data")

class BroadcastResponse(SuccessResponse):
    """Response model for broadcast creation."""
    data: Dict[str, Any] = Field(..., description="Broadcast creation result data")

class ContentTemplate(BaseModel):
    """Model for a content template in ManyChat."""
    id: str = Field(..., description="Unique identifier for the template")
    name: str = Field(..., description="Name of the template")
    content_type: str = Field(..., description="Type of content")
    content: Dict[str, Any] = Field(..., description="Template content")
    created_at: datetime = Field(..., description="When the template was created")
    updated_at: Optional[datetime] = Field(None, description="When the template was last updated")

class ContentTemplatesResponse(PaginatedResponse):
    """Response model for paginated list of content templates."""
    data: List[ContentTemplate] = Field(..., description="List of content templates")

class ContentTemplateResponse(SuccessResponse):
    """Response model for a single content template."""
    data: ContentTemplate = Field(..., description="Content template data")

class Webhook(BaseModel):
    """Model for a webhook configuration in ManyChat."""
    id: str = Field(..., description="Unique identifier for the webhook")
    url: HttpUrl = Field(..., description="URL where webhooks are sent")
    events: List[str] = Field(..., description="List of events that trigger the webhook")
    is_active: bool = Field(True, description="Whether the webhook is active")
    created_at: datetime = Field(..., description="When the webhook was created")
    updated_at: Optional[datetime] = Field(None, description="When the webhook was last updated")

class WebhooksResponse(PaginatedResponse):
    """Response model for paginated list of webhooks."""
    data: List[Webhook] = Field(..., description="List of webhook configurations")

class WebhookResponse(SuccessResponse):
    """Response model for webhook operations."""
    data: Webhook = Field(..., description="Webhook configuration data")

# Type aliases for better type hints
SubscriberId = str
TagId = str
CustomFieldId = str
FlowId = str
BroadcastId = str
TemplateId = str
WebhookId = str