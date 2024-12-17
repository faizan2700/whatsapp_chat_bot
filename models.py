from pydantic import BaseModel, Field
from typing import List, Optional

class TextMessage(BaseModel):
    """Represents a text message body."""
    body: str

class Contact(BaseModel):
    """Represents contact information."""
    profile: Optional[dict] = None
    wa_id: str

class Message(BaseModel):
    """Represents an individual message."""
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessage] = None

class Change(BaseModel):
    """Represents changes in the webhook payload."""
    field: str
    value: dict

class Entry(BaseModel):
    """Represents an entry in the webhook payload."""
    id: str
    changes: List[Change]

class WhatsAppWebhookPayload(BaseModel):
    """Represents the complete WhatsApp webhook payload."""
    object: str
    entry: List[Entry]

class MessageResponse(BaseModel):
    """Model for sending message response."""
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    to: str
    type: str = "text"
    text: dict