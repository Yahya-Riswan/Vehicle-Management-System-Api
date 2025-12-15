from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    address = Column(String(255), nullable=True)
    id_proof_type = Column(String(50), nullable=False)
    id_proof_number = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    supplied_bikes = relationship("Bike", back_populates="supplier")
