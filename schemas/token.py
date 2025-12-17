from pydantic import BaseModel
from .staff import StaffResponse
class Token(BaseModel):
    access_token: str
    token_type: str
    user: StaffResponse

class TokenData(BaseModel):
    username: str | None = None