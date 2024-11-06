from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import app.db.models
import app.schemas.schemas
from app.schemas.schemas import ProductStatus
from app.db.database import views_collection
from typing import List



load_dotenv()

# Função para criar um novo produto
def post_product(db: Session, product: app.schemas.schemas.ProductCreate) -> app.db.models.Product:

    status = ProductStatus(product.status)

    db_product = app.db.models.Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        status=status,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Função para ler todos os produtos e armazenar log visualização
def get_all_products(db: Session) -> List[app.schemas.schemas.ProductResponse]:
    products = db.query(app.db.models.Product).all()

    product_list = [
        app.schemas.schemas.ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price
        )
        for product in products
    ]

    # Armazenar no MongoDB as informações buscadas
    log_entry = {
        "product_ids": [product.id for product in products],
        "searched_at": datetime.now()
    }
    views_collection.insert_one(log_entry)

    return product_list

# Função para atualizar um produto existente
def put_product(db: Session, product_id: int, product: app.schemas.schemas.ProductUpdate) -> app.db.models.Product:
    db_product = db.query(app.db.models.Product).filter(app.db.models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.status = product.status
    db_product.stock_quantity = product.stock_quantity
    db.commit()
    db.refresh(db_product)
    
    return db_product

# Função para excluir um produto
def del_product(db: Session, product_id: int) -> app.db.models.Product:
    product = db.query(app.db.models.Product).filter(app.db.models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    # Excluir o log de visualizações do produto
    views_collection.delete_many({"product_ids": product_id})

    db.delete(product)
    db.commit()
    return JSONResponse(content={"message": "Item excluído com sucesso!"})

