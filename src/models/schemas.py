from pydantic import BaseModel
from typing import Optional

class ChatTextRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    text_reply: str
    emotion: str
    audio_url: Optional[str] = None

class LogoutRequest(BaseModel):
    user_id: str