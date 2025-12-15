from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db 
import auth
from models import staff as staff_model
router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# Create a new Customer
@router.post("/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    # Check if phone already exists
    existing_customer = db.query(models.Customer).filter(models.Customer.phone == customer.phone).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this phone number already exists")
    
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# Get all Customers
@router.get("/", response_model=List[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

# Get single Customer by ID
@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(customer_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Update Customer
@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update only provided fields
    update_data = customer_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Delete Customer
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return None