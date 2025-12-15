from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base schema with shared fields
class CustomerBase(BaseModel):
    type: str
    full_name: str
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    id_proof_type: Optional[str] = None
    id_proof_number: Optional[str] = None

# Schema for creating a customer (User input)
class CustomerCreate(CustomerBase):
    pass

# Schema for updating a customer (All fields optional)
class CustomerUpdate(BaseModel):
    type: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    id_proof_type: Optional[str] = None
    id_proof_number: Optional[str] = None

# Schema for reading a customer (Response output)
class CustomerResponse(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read data from ORM models