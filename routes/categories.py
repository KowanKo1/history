from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.models import Category
from app.crud import create_category, get_categories

router = APIRouter()

@router.post("/", response_model=Category)
def create_new_category(category: Category, db: Session = Depends(get_db)):
    return create_category(db, category)

@router.get("/", response_model=list[Category])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)
