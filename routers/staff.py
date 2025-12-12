from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import database
from schemas import staff as staff_schema
from models import staff as staff_model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.get("/", response_model=List[staff_schema.StaffResponse])
def get_all_staff(db: Session = Depends(database.get_db)):
 
    return db.query(staff_model.Staff).all()

@router.post("/register", response_model=staff_schema.StaffResponse, status_code=status.HTTP_201_CREATED)
def register(staff: staff_schema.StaffCreate, db: Session = Depends(database.get_db)):
    
    
    existing_user = db.query(staff_model.Staff).filter(staff_model.Staff.username == staff.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(staff.password)

    new_staff = staff_model.Staff(
        full_name=staff.full_name,
        role=staff.role,
        username=staff.username,
        phone=staff.phone,
        status=staff.status,
        password_hash=hashed_pw
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    
    return new_staff

@router.get("/login", response_model=staff_schema.StaffResponse)
def login(username: str, password: str, db: Session = Depends(database.get_db)):
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.username == username).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    if verify_password(password, staff_member.password_hash) is False:
         raise HTTPException(status_code=401, detail="Incorrect password")
    
    return staff_member

@router.get("/{staff_id}", response_model=staff_schema.StaffResponse)
def get_staff_by_id(staff_id: int, db: Session = Depends(database.get_db)):
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.id == staff_id).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    return staff_member

@router.put("/{staff_id}", response_model=staff_schema.StaffResponse)
def update_staff(staff_id: int, staff_update: staff_schema.StaffUpdate, db: Session = Depends(database.get_db)):
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.id == staff_id).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    for var, value in vars(staff_update).items():
        if value is not None:
            setattr(staff_member, var, value)
    
    db.commit()
    db.refresh(staff_member)
    
    return staff_member

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(staff_id: int, db: Session = Depends(database.get_db)):
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.id == staff_id).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    db.delete(staff_member)
    db.commit()
    
    return