from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # Import this to run raw SQL
from database import get_db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

@app.get("/")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Run a simple query that doesn't need any tables to exist
        result = db.execute(text("SELECT 1")).scalar()
        
        if result == 1:
            return {"status": "success", "message": "Successfully connected to SQL Server!"}
        
    except Exception as e:
        # If anything goes wrong, catch the error and show it
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed! Error: {str(e)}"
        )