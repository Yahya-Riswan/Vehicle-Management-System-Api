from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import ssl  
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('TIDB_USER')}:{os.getenv('TIDB_PASSWORD')}"
    f"@{os.getenv('TIDB_HOST')}:{os.getenv('TIDB_PORT', '4000')}"  
    f"/{os.getenv('TIDB_DATABASE', 'test')}?charset=utf8mb4"    
)

connect_args = {}


if os.path.exists("/etc/ssl/certs/ca-certificates.crt"):
    
    connect_args["ssl"] = {
        "ca": "/etc/ssl/certs/ca-certificates.crt"
    }
else:

    connect_args["ssl"] = {
        "check_hostname": False,
        "verify_mode": ssl.CERT_NONE
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args, 
    pool_recycle=3600,       
    pool_pre_ping=True        
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()