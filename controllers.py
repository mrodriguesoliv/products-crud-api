import models
import os
import schemas
from datetime import datetime
from pymongo import MongoClient
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv


# Conexão com MongoDB
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_DETAILS)
db = client.products_logs

# Função para visualizar o log do produto
def log_product_view(product_id: int):
    # Inserir um log de visualização
    db.product_views.insert_one({
        "product_id": product_id,
        "viewed_at": datetime.now()
    })

# Função para criar um novo produto
def post_product(db: Session, product: schemas.ProductCreate):
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
    print(db_product)
    return db_product

# Função para ler todos os produtos e registrar visualizações
def get_all_products(db: Session):
    products = db.query(models.Product).all()

    # Gera a lista de produtos como dicionários
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
        for product in products
    ]

    return product_list

# Função para ler um produto por ID e registrar visualização
def get_product_id(db: Session, product_id: int):
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
def put_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.status = product.status
        db_product.stock_quantity = product.stock_quantity
        db.commit()
        db.refresh(db_product)
    return db_product

# Função para excluir um produto
def del_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product
