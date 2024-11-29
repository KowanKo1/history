from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.models import Item
from app.crud import create_item, get_items, update_stock

router = APIRouter()

@router.post("/", response_model=Item)
def create_new_item(item: Item, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/", response_model=list[Item])
def read_items(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_items(db, category_id)

@router.put("/{item_id}/update_stock", response_model=Item)
def modify_stock(item_id: int, quantity: int, transaction_type: str, db: Session = Depends(get_db)):
    try:
        return update_stock(db, item_id, quantity, transaction_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
