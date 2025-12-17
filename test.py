from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    # This will list all columns in the 'sales' table
    result = conn.execute(text("DESCRIBE sales;"))
    print("\n--- COLUMNS IN TiDB SALES TABLE ---")
    for row in result:
        print(row[0]) # Prints column name
    print("-----------------------------------")