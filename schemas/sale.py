from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .bike import BikeResponse
from .customer import CustomerResponse
from .staff import StaffResponse

# ---------------------------------------------------------
# 1. BASE SCHEMA (Shared Fields)
# ---------------------------------------------------------
class SaleBase(BaseModel):
    sale_date: Optional[date] = None
    final_sale_price: float
    amount_cash: Optional[float] = 0.0
    amount_online: Optional[float] = 0.0
    amount_financed: Optional[float] = 0.0
    finance_company: Optional[str] = None
    warranty_months: Optional[int] = 0
    warranty_expires: Optional[date] = None
    rto_status: Optional[str] = "Pending"
    rto_agent_name: Optional[str] = None

# ---------------------------------------------------------
# 2. CREATE SCHEMA (Input = Integers)
# ---------------------------------------------------------
class SaleCreate(SaleBase):
    bike_id: int       # <--- Input expects ID (1)
    customer_id: int   # <--- Input expects ID (5)
    salesman_id: int   # <--- Input expects ID (2)

# ---------------------------------------------------------
# 3. UPDATE SCHEMA
# ---------------------------------------------------------
class SaleUpdate(BaseModel):
    final_sale_price: Optional[float] = None
    amount_cash: Optional[float] = None
    amount_online: Optional[float] = None
    amount_financed: Optional[float] = None
    finance_company: Optional[str] = None
    rto_status: Optional[str] = None
    rto_agent_name: Optional[str] = None

# ---------------------------------------------------------
# 4. RESPONSE SCHEMA (Output = Nested Objects)
# ---------------------------------------------------------
class SaleResponse(SaleBase):
    sale_id: int
    
    # These match the relationship names in models.py
    bike: Optional[BikeResponse] = None          # <--- Output gives full Bike details
    customer: Optional[CustomerResponse] = None  # <--- Output gives full Customer details
    salesman: Optional[StaffResponse] = None     # <--- Output gives full Staff details

    # Optional: Include raw IDs if needed
    bike_id: int
    customer_id: int
    salesman_id: int

    class Config:
        from_attributes = True