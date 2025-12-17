from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from .bike_images import BikeImageResponse
# Shared properties
class BikeBase(BaseModel):
    make: str
    model: str
    variant: Optional[str] = None
    mfg_year: Optional[int] = None
    color: Optional[str] = None
    odometer_km: Optional[int] = None
    reg_number: str
    chassis_number: str
    engine_number: str
    type:str
    owner_serial: Optional[str] = None
    insurance_valid_till: Optional[date] = None
    puc_valid_till: Optional[date] = None
    noc_status: Optional[str] = None
    supplier_id: Optional[int] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[date] = None
    listing_price: Optional[float] = None
    min_selling_price: Optional[float] = None
    status: Optional[str] = "Available"
    location_in_shop: Optional[str] = None


# Schema for creating a bike (User input)
class BikeCreate(BikeBase):
    pass

# Schema for updating a bike (All fields optional)
class BikeUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    variant: Optional[str] = None
    mfg_year: Optional[int] = None
    color: Optional[str] = None
    odometer_km: Optional[int] = None
    reg_number: Optional[str] = None
    chassis_number: Optional[str] = None
    engine_number: Optional[str] = None
    owner_serial: Optional[str] = None
    insurance_valid_till: Optional[date] = None
    puc_valid_till: Optional[date] = None
    noc_status: Optional[str] = None
    supplier_id: Optional[int] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[date] = None
    listing_price: Optional[float] = None
    min_selling_price: Optional[float] = None
    status: Optional[str] = None
    location_in_shop: Optional[str] = None

# Schema for reading a bike (Response output)
class BikeResponse(BikeBase):
    bike_id: int
    make: str
    model: str
    variant: Optional[str] = None
    mfg_year: Optional[int] = None
    color: Optional[str] = None
    odometer_km: Optional[int] = None
    type: Optional[str] = None
    insurance_valid_till: Optional[date] = None
    puc_valid_till: Optional[date] = None
    listing_price: Optional[float] = None
    owner_serial: Optional[str] = None
    # This list will automatically grab data from the 'images' relationship
    images: List[BikeImageResponse] = [] 

    class Config:
        from_attributes = True