from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    bike_id = Column(Integer, ForeignKey("bikes.bike_id"), unique=True, nullable=False) # One bike can only be sold once
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    salesman_id = Column(Integer, ForeignKey("staff.staff_id"), nullable=True) # Assuming you have a staff table

    # Sale Details
    sale_date = Column(Date, server_default=func.current_date())
    final_sale_price = Column(Float, nullable=False)
    
    # Payment Split
    amount_cash = Column(Float, default=0.0)
    amount_online = Column(Float, default=0.0)
    amount_financed = Column(Float, default=0.0)
    finance_company = Column(String, nullable=True)
    
    # Post Sale
    warranty_months = Column(Integer, default=0)
    warranty_expires = Column(Date, nullable=True)
    
    rto_status = Column(String, default="Pending") # e.g., Pending, Applied, Completed
    rto_agent_name = Column(String, nullable=True)

    # Relationship Back-refs
    bike = relationship("Bike", backref="sale_info")
    customer = relationship("Customer", backref="purchases")
    salesman = relationship("Staff", backref="sales_made") # Ensure Staff model exists