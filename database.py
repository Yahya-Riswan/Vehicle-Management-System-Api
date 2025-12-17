from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Define connection args based on the database type
connect_args = {}

# # SQLite needs this, but MySQL/TiDB does NOT.
# if "sqlite" in SQLALCHEMY_DATABASE_URL:
#     connect_args = {"check_same_thread": False}

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True  # Keeps the connection alive for cloud databases
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()