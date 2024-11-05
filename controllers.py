from pymongo.errors import PyMongoError
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
import models
import schemas
from database import views_collection
from typing import List


load_dotenv()

# Função para criar um novo produto
def post_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(
        id=product.id,
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

# Função para ler todos os produtos
def get_all_products(db: Session) -> List[schemas.ProductResponse]:
    products = db.query(models.Product).all()

    product_list = [
        schemas.ProductResponse(
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

# Função para ler um produto por ID
def get_product_id(db: Session, product_id: int) -> dict:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if product:

        product_detail = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        return product_detail

    raise HTTPException(status_code=404, detail="Produto não existe")

# Função para atualizar um produto existente
def put_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> models.Product:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
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
def del_product(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    db.delete(product)
    db.commit()
    return product

