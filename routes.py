from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductResponse
from database import get_db
from controllers import  get_all_products, get_product_id, post_product, put_product, del_product

router = APIRouter()

# Criar um novo produto
@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product = post_product(db, product)
    return product

# Ler todos os produtos
@router.get("/products/", response_model=list[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

# Ler um produto específico por ID
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
   product = get_product_id(db, product_id)
   return product

# Atualizar um produto
@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    product = put_product(db, product_id, product)
    return product

# Excluir um produto
@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = del_product(db, product_id)
    return product
