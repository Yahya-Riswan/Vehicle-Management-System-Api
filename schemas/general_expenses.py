from pydantic import BaseModel
from typing import List, Optional
from datetime import date
# ---------------------------------------------------------
# GENERAL EXPENSE SCHEMAS (New)
# ---------------------------------------------------------
class GeneralExpenseBase(BaseModel):
    title: str
    category: str
    amount: float
    expense_date: date
    paid_to: Optional[str] = None
    payment_mode: Optional[str] = None

class GeneralExpenseCreate(GeneralExpenseBase):
    pass

class GeneralExpenseUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    paid_to: Optional[str] = None
    payment_mode: Optional[str] = None

class GeneralExpenseResponse(GeneralExpenseBase):
    id: int

    class Config:
        from_attributes = True