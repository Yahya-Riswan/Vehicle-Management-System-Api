from pydantic import BaseModel
from typing import List, Optional
from datetime import date
class BikeExpenseBase(BaseModel):
    type: str 
    description: Optional[str] = None
    cost: float
    expense_date: date
    performed_by: Optional[str] = None

class BikeExpenseCreate(BikeExpenseBase):
    pass

# --- NEW: ADD THIS CLASS ---
class BikeExpenseUpdate(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    expense_date: Optional[date] = None
    performed_by: Optional[str] = None

# --- EXISTING RESPONSE ---
class BikeExpenseResponse(BikeExpenseBase):
    expense_id: int
    bike_id: int

    class Config:
        from_attributes = True
        
