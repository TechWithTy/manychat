"""Base request models for ManyChat API."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, validator

from ._base import BaseRequest


class FieldType(str, Enum):
    """Types of custom fields in ManyChat."""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    COUNTRY = "country"
    TIMEZONE = "timezone"


class Tag(BaseModel):
    """Tag model for ManyChat."""
    tag_id: int = Field(..., alias="id", description="Unique identifier for the tag")
    name: str = Field(..., description="Name of the tag")
    description: Optional[str] = Field(None, description="Optional description")
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class SubscriberField(BaseModel):
    """Subscriber field model for ManyChat."""
    id: int = Field(..., description="Field ID")
    field_id: int = Field(..., alias="fieldId", description="Field ID alias")
    name: str = Field(..., description="Field name")
    type: FieldType = Field(..., description="Field type")
    description: Optional[str] = Field(None, description="Field description")
    value: Any = Field(None, description="Field value")
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class Subscriber(BaseModel):
    """Subscriber model for ManyChat."""
    id: str = Field(..., description="Subscriber ID")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    name: Optional[str] = None
    gender: Optional[Literal["male", "female", "unknown"]] = None
    profile_pic: Optional[HttpUrl] = Field(None, alias="profilePic")
    locale: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[int] = None
    last_input_text: Optional[str] = Field(None, alias="lastInputText")
    last_interaction: Optional[str] = Field(None, alias="lastInteraction")
    last_seen: Optional[str] = Field(None, alias="lastSeen")
    last_user_text: Optional[str] = Field(None, alias="lastUserText")
    subscribed: Optional[bool] = None
    utm_campaign: Optional[str] = Field(None, alias="utmCampaign")
    utm_content: Optional[str] = Field(None, alias="utmContent")
    utm_medium: Optional[str] = Field(None, alias="utmMedium")
    utm_source: Optional[str] = Field(None, alias="utmSource")
    utm_term: Optional[str] = Field(None, alias="utmTerm")
    user_phone: Optional[str] = Field(None, alias="userPhone")
    whatsapp_phone: Optional[str] = Field(None, alias="whatsappPhone")
    whatsapp_phone_id: Optional[str] = Field(None, alias="whatsappPhoneId")
    
    # Relationships
    tags: List[Tag] = Field(default_factory=list, description="List of tags")
    fields: List[SubscriberField] = Field(default_factory=list, description="Custom fields")
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class GetSubscriberInfoRequest(BaseRequest):
    """Request model for getting subscriber information."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    fields: Optional[List[str]] = Field(
        None,
        description="List of field names to include in the response"
    )
    
    class Config:
        allow_population_by_field_name = True


class AddTagByNameRequest(BaseRequest):
    """Request model for adding a tag to a subscriber by name."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    tag_name: str = Field(..., alias="tagName", description="Name of the tag to add")
    
    class Config:
        allow_population_by_field_name = True


class RemoveTagRequest(BaseRequest):
    """Request model for removing a tag from a subscriber."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    tag_id: int = Field(..., alias="tagId", description="ID of the tag to remove")
    
    class Config:
        allow_population_by_field_name = True


class SetCustomFieldRequest(BaseRequest):
    """Request model for setting a custom field value."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    field_id: Union[str, int] = Field(..., alias="fieldId", description="Field ID or name")
    field_value: Any = Field(..., alias="fieldValue", description="Value to set")
    
    class Config:
        allow_population_by_field_name = True


class SendContentRequest(BaseRequest):
    """Request model for sending content to a subscriber."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    message_tag: Optional[str] = Field(
        None,
        alias="messageTag",
        description="Optional tag for the message"
    )
    
    class Config:
        allow_population_by_field_name = True


class SendFlowRequest(BaseRequest):
    """Request model for triggering a flow for a subscriber."""
    subscriber_id: str = Field(..., alias="subscriberId", description="Subscriber ID")
    flow_ns: str = Field(..., alias="flowNs", description="Flow namespace")
    
    class Config:
        allow_population_by_field_name = True


class BroadcastRequest(BaseRequest):
    """Request model for sending a broadcast."""
    messages: List[Dict[str, Any]] = Field(..., description="List of message objects")
    messages_operator: Literal["or", "and"] = Field(
        "or",
        alias="messagesOperator",
        description="Logical operator for multiple messages"
    )
    send_to_chatboxes: bool = Field(
        True,
        alias="sendToChatboxes",
        description="Whether to send to chat boxes"
    )
    send_to_smart_inbox: bool = Field(
        True,
        alias="sendToSmartInbox",
        description="Whether to send to smart inbox"
    )
    
    class Config:
        allow_population_by_field_name = True


class GetTagsRequest(BaseRequest):
    """Request model for getting all tags."""
    limit: Optional[int] = Field(100, description="Maximum number of tags to return")
    after: Optional[str] = Field(None, description="Cursor for pagination")
    
    class Config:
        allow_population_by_field_name = True