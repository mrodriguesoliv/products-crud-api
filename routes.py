from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductCreate, ProductResponse, ProductWithLogs, ProductLog
from database import get_db, views_collection
from controllers import get_all_products, get_product_id, post_product, put_product, del_product
from models import Product

router = APIRouter()

# Criar um novo produto
@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return post_product(db, product)

# Ler todos os produtos
@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    return get_all_products(db)

# Ler um produto específico por ID
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_id(db, product_id)

# Atualizar um produto
@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    return put_product(db, product_id, product)

# Excluir um produto 
@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return del_product(db, product_id)

# Ler um produto por ID com log de visualização
@router.get("/products/logs/{product_id}", response_model=ProductWithLogs)
def read_product_with_logs(product_id: int, db: Session = Depends(get_db)):
    # Obter as informações do produto
    product_teste = db.query(Product).filter(Product.id == product_id).first()
    
    if not product_teste:
        raise HTTPException(status_code=404, detail="Product not found")

    # Obter o log de buscas para o produto no MongoDB
    logs = list(views_collection.find({"product_ids": product_id}))
    
    # Formatar os logs
    product_logs = [
        ProductLog(searched_at=log['searched_at']) for log in logs
    ]

    # Criar a resposta
    response = ProductWithLogs(
        id=product_teste.id,
        name=product_teste.name,
        description=product_teste.description,
        price=product_teste.price,
        logs=product_logs
    )
    
    return response