from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
import auth
from models import staff as staff_model
router = APIRouter(tags=["Bikes"])



# --- NEW: Add an Image to a Bike ---
@router.post("/bikes/{bike_id}/images", response_model=schemas.BikeImageResponse)
def add_bike_image(bike_id: int, image: schemas.BikeImageCreate,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    
    
    # 1. Verify Bike exists
    bike = db.query(models.Bike).filter(models.Bike.bike_id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    # 2. Create Image Record
    # Note: This assumes you have already uploaded the file to Cloudinary 
    # and are sending the resulting URL here.
    new_image = models.BikeImage(
        bike_id=bike_id,
        image_url=image.image_url,
        cloudinary_public_id=image.cloudinary_public_id,
        is_primary=image.is_primary
    )
    
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

# --- NEW: Delete an Image ---
@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bike_image(image_id: int,db: Session = Depends(get_db),
    current_user: staff_model.Staff = Depends(auth.get_current_user)):
    
    
    image = db.query(models.BikeImage).filter(models.BikeImage.image_id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    db.delete(image)
    db.commit()
    return None