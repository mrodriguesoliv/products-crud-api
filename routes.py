from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductResponse
from database import get_db
from controllers import  get_all_products


router = APIRouter()

# Criar um novo produto
@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        status=product.status,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Ler um produto específico por ID
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Ler todos os produtos
@router.get("/products/", response_model=list[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    return get_all_products(db)

# Atualizar um produto
@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.status = product.status
    db_product.stock_quantity = product.stock_quantity

    db.commit()
    db.refresh(db_product)
    return db_product

# Excluir um produto
@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product
