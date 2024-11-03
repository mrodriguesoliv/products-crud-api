import models
import schemas
from datetime import datetime
from pymongo import MongoClient
from sqlalchemy.orm import Session


# Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.products_logs
views_collection = db.views_log

# Função para visualizar o log do produto
def log_product_view(product_id):
    view_data = {
        "product_id": product_id,
        "timestamp": datetime.utcnow()
    }
    views_collection.insert_one(view_data)

# Função para criar um novo produto
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
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

# Função para ler um produto por ID e registrar visualização
def read_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        log_product_view(product_id)
        return {
            "name": product.name,
            "description": product.description,
            "price": product.price
        }
    return None

# Função para ler todos os produtos e registrar visualizações
def get_all_products(db: Session):
    # Recupera todos os produtos do banco de dados
    products = db.query(models.Product).all()
    product_list = []

    for product in products:
        log_product_view(product.id)
        product_list.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        })
    
    return product_list

# Função para atualizar um produto existente
def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.status = product.status
        db_product.stock_quantity = product.stock_quantity
        db.commit()
        db.refresh(db_product)
    return db_product

# Função para excluir um produto
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
