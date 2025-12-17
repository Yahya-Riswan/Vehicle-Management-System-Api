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

