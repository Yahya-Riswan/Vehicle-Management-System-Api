from fastapi import FastAPI
import database
import models
from routers import staff,bike,bike_images,customer,bike_expenses,general_expenses,sale
from fastapi.middleware.cors import CORSMiddleware

database.Base.metadata.create_all(bind=database.engine)


app = FastAPI(
    title="Vehicle Management API",
    description="This API handles staff management, vehicle inventory, and sales tracking for the  used bike shop.",
    version="1.0.0",
    contact={
        "name": "Zypher Studio X Support",
        "email": "zypherstudio.x@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],          # Allow all headers
)
app.include_router(staff.router)
app.include_router(bike.router)
app.include_router(bike_images.router)
app.include_router(customer.router)
app.include_router(bike_expenses.router)
app.include_router(general_expenses.router)
app.include_router(sale.router)
@app.get("/")
def root():
    return {"message": "Bike Shop API is running!"}