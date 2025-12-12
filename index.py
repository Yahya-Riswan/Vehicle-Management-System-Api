from fastapi import FastAPI
import database
import models
from routers import staff

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(staff.router)

@app.get("/")
def root():
    return {"message": "Bike Shop API is running!"}