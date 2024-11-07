from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import ProductCreate, ProductResponse, ProductWithLogs, ProductLog
from app.db.database import get_db, views_collection
from app.controllers.controllers import get_all_products, post_product, put_product, del_product
from app.db.models import Product

router = APIRouter()

@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Cria um novo produto no banco de dados."""
    return post_product(db, product)

@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    """Retorna uma lista de todos os produtos."""
    return get_all_products(db)

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    """Atualiza as informações de um produto existente."""
    return put_product(db, product_id, product)

@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Exclui um produto pelo ID."""
    return del_product(db, product_id)

@router.get("/products/logs/{product_id}", response_model=ProductWithLogs)
def read_product_with_logs(product_id: int, db: Session = Depends(get_db)):
    """Retorna informações do produto junto com os logs de visualização."""
    product_teste = db.query(Product).filter(Product.id == product_id).first()
    
    if not product_teste:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    logs = list(views_collection.find({"product_ids": product_id}))
    
    product_logs = [
        ProductLog(searched_at=log['searched_at']) for log in logs
    ]

    response = ProductWithLogs(
        id=product_teste.id,
        name=product_teste.name,
        description=product_teste.description,
        price=product_teste.price,
        logs=product_logs
    )
    
    return response
