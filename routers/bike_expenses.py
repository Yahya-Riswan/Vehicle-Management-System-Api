from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models # Adjust dots based on your folder structure
import schemas 
from database import get_db
import auth
from models import staff as staff_model
router = APIRouter(
    prefix="/expenses",
    tags=["Bike Expenses"]
)

# 1. Add an Expense to a Bike
@router.post("/{bike_id}", response_model=schemas.BikeExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(bike_id: int, expense: schemas.BikeExpenseCreate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    # Verify bike exists first
    bike = db.query(models.Bike).filter(models.Bike.bike_id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    new_expense = models.BikeExpense(
        bike_id=bike_id,
        **expense.dict()
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# 2. Get all expenses for a specific Bike
@router.get("/{bike_id}", response_model=List[schemas.BikeExpenseResponse])
def read_bike_expenses(bike_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    expenses = db.query(models.BikeExpense).filter(models.BikeExpense.bike_id == bike_id).all()
    return expenses

# 3. Delete an Expense
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    expense = db.query(models.BikeExpense).filter(models.BikeExpense.expense_id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return None

# 4. Update an Expense
@router.put("/{expense_id}", response_model=schemas.BikeExpenseResponse)
def update_expense(expense_id: int, expense_update: schemas.BikeExpenseUpdate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    # 1. Find the expense
    db_expense = db.query(models.BikeExpense).filter(models.BikeExpense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # 2. Update only the fields sent by the user
    update_data = expense_update.dict(exclude_unset=True) # exclude_unset=True ensures we don't overwrite data with nulls
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    # 3. Save changes
    db.commit()
    db.refresh(db_expense)
    return db_expense