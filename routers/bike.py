from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
import auth
from models import staff as staff_model
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from sqlalchemy import desc, asc, or_
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





@router.get("/", response_model=List[schemas.BikeResponse])
def read_bikes(
    db: Session = Depends(get_db),
    # Search & Filters
    q: Optional[str] = Query(None, description="Search by Name or Make"),
    type: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    # Pagination
    page: int = 1,
    limit: int = 10
):
    # 1. Start Query
    query = db.query(models.Bike)

    # 2. MANDATORY FILTER: Only show "Available" status
    query = query.filter(models.Bike.status == "Available")

    # 3. Apply Search (Optional)
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.Bike.make.ilike(search),
                models.Bike.model.ilike(search) # Changed from 'name' to 'model' based on your new schema
            )
        )

    # 4. Apply Filters (Optional)
    if type:
        query = query.filter(models.Bike.type == type)
    if brand:
        query = query.filter(models.Bike.make == brand)

    # 5. Load Images Efficiently
    # This tells SQLAlchemy to fetch the related images in a separate efficient query
    query = query.options(selectinload(models.Bike.images))

    # 6. Sorting
    if sort == "low":
        query = query.order_by(asc(models.Bike.listing_price)) # Assuming you want to sort by listing_price
    elif sort == "high":
        query = query.order_by(desc(models.Bike.listing_price))
    else:
        query = query.order_by(desc(models.Bike.bike_id))

    # 7. Pagination
    skip = (page - 1) * limit
    bikes = query.offset(skip).limit(limit).all()

    return bikes
@router.get("/admin", response_model=List[schemas.BikeResponse])
def read_bikes(
    db: Session = Depends(get_db),
    # Search & Filters
    q: Optional[str] = Query(None, description="Search by Name or Make"),
    type: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    # Pagination
    page: int = 1,
    limit: int = 10
):
    # 1. Start Query
    query = db.query(models.Bike)


    # 3. Apply Search (Optional)
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.Bike.make.ilike(search),
                models.Bike.model.ilike(search) # Changed from 'name' to 'model' based on your new schema
            )
        )

    # 4. Apply Filters (Optional)
    if type:
        query = query.filter(models.Bike.type == type)
    if brand:
        query = query.filter(models.Bike.make == brand)

    # 5. Load Images Efficiently
    # This tells SQLAlchemy to fetch the related images in a separate efficient query
    query = query.options(selectinload(models.Bike.images))

    # 6. Sorting
    if sort == "low":
        query = query.order_by(asc(models.Bike.listing_price)) # Assuming you want to sort by listing_price
    elif sort == "high":
        query = query.order_by(desc(models.Bike.listing_price))
    else:
        query = query.order_by(desc(models.Bike.bike_id))

    # 7. Pagination
    skip = (page - 1) * limit
    bikes = query.offset(skip).limit(limit).all()

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