from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.models import Transaction
from app.crud import get_transactions

router = APIRouter()

@router.get("/", response_model=list[Transaction])
def read_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)
