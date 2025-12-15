from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
import auth
from models import staff as staff_model
router = APIRouter(
    prefix="/bikes",
    tags=["Bikes"]
)

# Create a new Bike
@router.post("/", response_model=schemas.BikeResponse, status_code=status.HTTP_201_CREATED)
def create_bike(bike: schemas.BikeCreate, 
                db: Session = Depends(get_db),
                current_user: staff_model.Staff = Depends(auth.get_current_user) 
                ):
    
    
    # Check for duplicate registration number
    existing_bike = db.query(models.Bike).filter(models.Bike.reg_number == bike.reg_number).first()
    if existing_bike:
        raise HTTPException(status_code=400, detail="Bike with this Registration Number already exists")

    new_bike = models.Bike(**bike.dict())
    db.add(new_bike)
    db.commit()
    db.refresh(new_bike)
    return new_bike

# Get all Bikes
@router.get("/", response_model=List[schemas.BikeResponse])
def read_bikes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bikes = db.query(models.Bike).offset(skip).limit(limit).all()
    return bikes

# Get single Bike by ID
@router.get("/{bike_id}", response_model=schemas.BikeResponse)
def read_bike(bike_id: int, db: Session = Depends(get_db)):
    bike = db.query(models.Bike).filter(models.Bike.bike_id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike

# Update Bike
@router.put("/{bike_id}", response_model=schemas.BikeResponse)
def update_bike(bike_id: int, bike_update: schemas.BikeUpdate, db: Session = Depends(get_db),current_user: staff_model.Staff = Depends(auth.get_current_user) ):
    
    
    db_bike = db.query(models.Bike).filter(models.Bike.bike_id == bike_id).first()
    if not db_bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    update_data = bike_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bike, key, value)
    
    db.commit()
    db.refresh(db_bike)
    return db_bike

# Delete Bike
@router.delete("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bike(bike_id: int, db: Session = Depends(get_db),current_user: staff_model.Staff = Depends(auth.get_current_user) ):
    
    db_bike = db.query(models.Bike).filter(models.Bike.bike_id == bike_id).first()
    if not db_bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    db.delete(db_bike)
    db.commit()
    return None