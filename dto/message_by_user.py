from pydantic import BaseModel
from typing import Optional

class MessageByUserDto(BaseModel):
    email: str
    message: str
    status_message: str
    hour: str
    is_bot: bool #contrario a is_response
    audio: Optional[str] = None
    video: Optional[str] = None
    
