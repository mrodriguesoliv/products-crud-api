from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import Product
from .database import get_db

router = APIRouter()

@router.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/products/")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
