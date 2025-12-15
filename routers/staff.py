from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

# Import everything from our new structure
import database
from schemas import staff as staff_schema
from schemas import token as token_schema
from models import staff as staff_model
import auth 

router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)


@router.get("/", response_model=List[staff_schema.StaffResponse])
def get_all_staff(
    db: Session = Depends(database.get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user) 
):
    return db.query(staff_model.Staff).all()

@router.post("/register", response_model=staff_schema.StaffResponse, status_code=status.HTTP_201_CREATED)
def register(staff: staff_schema.StaffCreate, db: Session = Depends(database.get_db)):
    
    existing_user = db.query(staff_model.Staff).filter(staff_model.Staff.username == staff.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    
    hashed_pw = auth.hash_password(staff.password)

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


@router.post("/login", response_model=token_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.username == form_data.username).first()
    

    if not staff_member or not auth.verify_password(form_data.password, staff_member.password_hash):
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, 
             detail="Incorrect username or password",
             headers={"WWW-Authenticate": "Bearer"},
         )
    
   
    access_token = auth.create_access_token(data={"sub": staff_member.username})
    
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/{staff_id}", response_model=staff_schema.StaffResponse)
def get_staff_by_id(
    staff_id: int, 
    db: Session = Depends(database.get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user) 
    ):
    
    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.id == staff_id).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    return staff_member

@router.put("/{staff_id}", response_model=staff_schema.StaffResponse)
def update_staff(
    staff_id: int,
    staff_update: staff_schema.StaffUpdate, 
    db: Session = Depends(database.get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user) 
    ):
    
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
def delete_staff(
    staff_id: int, 
    db: Session = Depends(database.get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user) 
    ):
    
    

    staff_member = db.query(staff_model.Staff).filter(staff_model.Staff.id == staff_id).first()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    db.delete(staff_member)
    db.commit()
    
    return