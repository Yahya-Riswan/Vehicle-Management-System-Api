from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StaffBase(BaseModel):
    full_name: str
    role: str
    username: str
    phone: Optional[str] = None
    status: bool = True

class StaffCreate(StaffBase):
    password: str 


class StaffResponse(StaffBase):
    staff_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class StaffUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[bool] = None
    password: Optional[str] = None
    