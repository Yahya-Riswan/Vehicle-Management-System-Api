from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BikeImage(Base):
    __tablename__ = "bike_images"

    image_id = Column(Integer, primary_key=True, index=True)
    bike_id = Column(Integer, ForeignKey("bikes.bike_id"))
    image_url = Column(String, nullable=False)
    cloudinary_public_id = Column(String, nullable=True) 
    is_primary = Column(Boolean, default=False) 
    
    bike = relationship("Bike", back_populates="images")

   