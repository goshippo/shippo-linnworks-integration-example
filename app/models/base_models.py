from pydantic import BaseModel
from typing import Optional, List, Any

class BaseRequest(BaseModel):
    authorization_token: Optional[str] = None

class BaseResponse(BaseModel):
    is_error: bool = False
    error_message: Optional[str] = None
    
    def __init__(self, error_message: str = None, **data):
        super().__init__(**data)
        if error_message:
            self.is_error = True
            self.error_message = error_message