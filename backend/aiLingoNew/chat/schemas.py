from datetime import datetime
from ninja import Schema

class ConversationSchema(Schema):
    id: int
    user_id: int
    language_id: int
    title: str
    created_at: datetime

class MessageSchema(Schema):
    id: int
    conversation_id: int
    sender: str
    content: str
    timestamp: datetime