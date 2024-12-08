from fastapi import FastAPI, Request, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, select
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from database import init_db, get_db  # Import your database utilities
from fastapi.middleware.cors import CORSMiddleware
import os
from models import Transaction

# Load environment variables
load_dotenv()
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
AUTHENTICATION_SERVICE_URL = os.getenv("AUTHENTICATION_SERVICE_URL")

# Initialize database
init_db()

app = FastAPI()

@app.post("/api/transactions", response_model=Transaction)
async def create_transaction(
    transaction: Transaction,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Endpoint to create a transaction. Only accessible from INVENTORY_URL.
    """
    # print(request.headers)
    # print(request.headers.get('origin'))
    # print(INVENTORY_URL)
    if request.headers.get('origin') != INVENTORY_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    
    print('transaction received: ', transaction)
    
    transaction.createdAt = datetime.now()
    transaction.modifiedAt = datetime.now()
    transaction.timestamp = datetime.now()

    # Add the transaction to the database
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all transactions.
    """
    if request.headers.get('origin') != AUTHENTICATION_SERVICE_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")
    return db.exec(select(Transaction)).all()
