from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
import auth
from models import staff as staff_model
router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# 1. Create a New Sale (Sell a Bike)
@router.post("/", response_model=schemas.SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale: schemas.SaleCreate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    # A. Check if Bike exists and is available
    bike = db.query(models.Bike).filter(models.Bike.bike_id == sale.bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    if bike.status == "Sold":
        raise HTTPException(status_code=400, detail="This bike is already sold!")

    # B. Create Sale Record
    new_sale = models.Sale(**sale.dict())
    db.add(new_sale)
    
    # C. Update Bike Status to "Sold"
    bike.status = "Sold"
    
    db.commit()
    db.refresh(new_sale)
    return new_sale

# 2. Get All Sales
@router.get("/", response_model=List[schemas.SaleResponse])
def read_sales(skip: int = 0, limit: int = 100,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

# 3. Get Single Sale
@router.get("/{sale_id}", response_model=schemas.SaleResponse)
def read_sale(sale_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    sale = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale record not found")
    return sale

# 4. Update Sale Details (e.g., Update RTO status)
@router.put("/{sale_id}", response_model=schemas.SaleResponse)
def update_sale(sale_id: int, sale_update: schemas.SaleUpdate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    db_sale = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale record not found")
    
    update_data = sale_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sale, key, value)
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

# 5. Delete a Sale (Cancel a Sale)
@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    # 1. Find the sale
    sale = db.query(models.Sale).filter(models.Sale.sale_id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale record not found")
    
    # 2. Revert the Bike Status to "Available"
    # We access the bike using the relationship defined in models
    bike = db.query(models.Bike).filter(models.Bike.bike_id == sale.bike_id).first()
    if bike:
        bike.status = "Available"

    # 3. Delete the Sale Record
    db.delete(sale)
    db.commit()
    
    return None