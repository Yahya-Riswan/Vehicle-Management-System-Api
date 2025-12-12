from sqlalchemy import Column, Integer, String,  Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    status = Column(Boolean, default=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())