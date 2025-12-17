from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Bike(Base):
    __tablename__ = "bikes"

    bike_id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    variant = Column(String, nullable=True)
    mfg_year = Column(Integer, nullable=True)
    color = Column(String, nullable=True)
    odometer_km = Column(Integer, nullable=True)
    type = Column(String(20), nullable=True)
    owner_serial = Column(String(50), nullable=True)
    # Registration & Legal 
    reg_number = Column(String, unique=True, index=True, nullable=False)
    chassis_number = Column(String, unique=False, nullable=True)
    engine_number = Column(String, unique=False, nullable=True)
    owner_serial = Column(Integer, nullable=True) # e.g., 1st owner, 2nd owner
    
    # Dates
    insurance_valid_till = Column(Date, nullable=True)
    puc_valid_till = Column(Date, nullable=True)
    noc_status = Column(String, nullable=True)
    
    # Sourcing & Pricing (from second image)
    supplier_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    purchase_price = Column(Float, nullable=True)
    purchase_date = Column(Date, nullable=True)
    listing_price = Column(Float, nullable=True)
    min_selling_price = Column(Float, nullable=True)
    
    # Status & Location
    status = Column(String, default="Available") # e.g., Available, Sold, Reserved
    location_in_shop = Column(String, nullable=True)
    
    supplier = relationship("Customer", back_populates="supplied_bikes")
    
    # New: Link to images
    images = relationship("BikeImage", back_populates="bike", cascade="all, delete-orphan")
    
    expenses = relationship("BikeExpense", back_populates="bike", cascade="all, delete-orphan")