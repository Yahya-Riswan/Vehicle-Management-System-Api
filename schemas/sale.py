from pydantic import BaseModel
from typing import List, Optional
from datetime import date



# ---------------------------------------------------------
# SALE SCHEMAS
# ---------------------------------------------------------
class SaleBase(BaseModel):
    bike_id: int
    customer_id: int
    salesman_id: Optional[int] = None
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

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    final_sale_price: Optional[float] = None
    amount_cash: Optional[float] = None
    amount_online: Optional[float] = None
    amount_financed: Optional[float] = None
    finance_company: Optional[str] = None
    rto_status: Optional[str] = None
    rto_agent_name: Optional[str] = None
    # Add other fields if needed

class SaleResponse(SaleBase):
    sale_id: int
    
    class Config:
        from_attributes = True