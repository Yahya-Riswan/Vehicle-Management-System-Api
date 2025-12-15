from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BikeExpense(Base):
    __tablename__ = "bike_expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(Integer, ForeignKey("bikes.bike_id"), nullable=False)
    
    type = Column(String, nullable=False) # e.g., "Repair", "Service", "Fuel"
    description = Column(String, nullable=True)
    cost = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False)
    performed_by = Column(String, nullable=True) # e.g., Mechanic Name

    # Relationship back to Bike
    bike = relationship("Bike", back_populates="expenses")