from pydantic import BaseModel
from typing import List, Optional

# --- Image Schemas ---
class BikeImageBase(BaseModel):
    image_url: str
    cloudinary_public_id: Optional[str] = None
    is_primary: bool = False

class BikeImageCreate(BikeImageBase):
    pass

class BikeImageResponse(BikeImageBase):
    image_id: int
    bike_id: int

    class Config:
        from_attributes = True

# --- Bike Schemas ---
class BikeBase(BaseModel):
    make: str
    model: str
    # ... (other fields) ...

class BikeCreate(BikeBase):
    pass

class BikeResponse(BikeBase):
    bike_id: int
    # The API will now return a list of image objects inside the bike object
    images: List[BikeImageResponse] = [] 

    class Config:
        from_attributes = True