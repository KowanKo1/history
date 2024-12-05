from fastapi import FastAPI, Request, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, select
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from database import init_db, get_db  # Import your database utilities
from fastapi.middleware.cors import CORSMiddleware
import os

# Load environment variables
load_dotenv()
INVENTORY_URL = os.getenv("INVENTORY_URL")

# Initialize database
init_db()

app = FastAPI()

# Transaction model for the database
class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    item_id: int
    quantity: int
    transaction_type: str
    timestamp: datetime

@app.post("/api/transactions", response_model=Transaction)
async def create_transaction(
    transaction: Transaction,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Endpoint to create a transaction. Only accessible from INVENTORY_URL.
    """
    print(request.headers)
    print(request.headers.get('origin'))
    if request.headers.get('origin') != INVENTORY_URL:
        raise HTTPException(status_code=403, detail="Origin not allowed.")

    # Add the transaction to the database
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@app.get("/api/transactions", response_model=List[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all transactions.
    """
    return db.exec(select(Transaction)).all()
