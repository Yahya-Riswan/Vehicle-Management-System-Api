from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.sql import func
from database import Base

class GeneralExpense(Base):
    __tablename__ = "general_expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)      # e.g., "Shop Rent", "Electricity Bill"
    category = Column(String, nullable=False)   # e.g., "Utilities", "Salary", "Miscellaneous"
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False)
    paid_to = Column(String, nullable=True)     # e.g., "Landlord Name"
    payment_mode = Column(String, nullable=True) # e.g., "Cash", "UPI", "Bank Transfer"