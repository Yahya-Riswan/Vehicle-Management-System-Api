from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
import auth
from models import staff as staff_model
router = APIRouter(
    prefix="/general-expenses",
    tags=["General Expenses"]
)

# 1. Create a General Expense
@router.post("/", response_model=schemas.GeneralExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_general_expense(expense: schemas.GeneralExpenseCreate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    new_expense = models.GeneralExpense(**expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# 2. Get All General Expenses
@router.get("/", response_model=List[schemas.GeneralExpenseResponse])
def read_general_expenses(skip: int = 0, limit: int = 100,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    expenses = db.query(models.GeneralExpense).offset(skip).limit(limit).all()
    return expenses

# 3. Update a General Expense
@router.put("/{expense_id}", response_model=schemas.GeneralExpenseResponse)
def update_general_expense(expense_id: int, expense_update: schemas.GeneralExpenseUpdate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    db_expense = db.query(models.GeneralExpense).filter(models.GeneralExpense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

# 4. Delete a General Expense
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_general_expense(expense_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    expense = db.query(models.GeneralExpense).filter(models.GeneralExpense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return None