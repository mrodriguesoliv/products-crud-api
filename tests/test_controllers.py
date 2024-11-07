import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Product
from app.controllers.controllers import post_product, get_all_products, put_product, del_product
from app.schemas.schemas import ProductCreate, ProductUpdate, ProductStatus
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app')))

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    """Configura o banco de dados para os testes."""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def product(db):
    """Cria um produto de exemplo para os testes."""
    product = Product(id=1, name="Produto Teste", description="Descrição do produto", price=100.0, status=ProductStatus.in_stock, stock_quantity=10)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_post_product(db):
    """Teste de criação de um produto."""
    new_product_id = 1
    new_product_data = ProductCreate(
        id=new_product_id,
        name="Produto Criado", 
        description="Descrição do produto criado", 
        price=200.0, 
        status=ProductStatus.in_stock, 
        stock_quantity=20
    )
    
    product = post_product(db, new_product_data)

    assert product.id == new_product_id
    assert product.name == "Produto Criado"
    assert product.description == "Descrição do produto criado"
    assert product.price == 200.0
    assert product.status == ProductStatus.in_stock
    assert product.stock_quantity == 20

    del_product(db, product_id=1)

def test_get_all_products(db):
    """Teste de listagem de todos os produtos."""
    new_product_id = 1
    new_product = Product(
        id=new_product_id,
        name="Produto Único",
        description="Descrição do produto único",
        price=100.0,
        status=ProductStatus.in_stock,
        stock_quantity=10
    )
    db.add(new_product)
    db.commit()

    products = get_all_products(db)

    assert len(products) == 1
    assert products[0].name == "Produto Único"
    assert products[0].description == "Descrição do produto único"
    assert products[0].price == 100.0

    del_product(db, product_id=1)


def test_put_product(db):
    """Teste de atualização de um produto."""
    new_product_id = 1

    existing_product = Product(
        id=new_product_id,
        name="Produto Existente",
        description="Descrição existente",
        price=100.0,
        status=ProductStatus.in_stock,
        stock_quantity=5
    )
    db.add(existing_product)
    db.commit()

    updated_product_data = ProductUpdate(
        id=new_product_id,
        name="Produto Atualizado",
        description="Descrição atualizada",
        price=120.0,
        status=ProductStatus.out_of_stock,
        stock_quantity=8
    )

    updated_product = put_product(db, product_id=new_product_id, product=updated_product_data)

    assert updated_product.name == "Produto Atualizado"
    assert updated_product.description == "Descrição atualizada"
    assert updated_product.price == 120.0
    assert updated_product.status == ProductStatus.out_of_stock
    assert updated_product.stock_quantity == 8

    del_product(db, product_id=1)

def test_del_product(db):
    """Teste de exclusão de um produto."""
    new_product_id = 1

    db.query(Product).filter(Product.id == new_product_id).delete()
    db.commit()

    product_to_delete = Product(
        id=new_product_id,
        name="Produto para Exclusão",
        description="Descrição do produto a ser excluído",
        price=50.0,
        status=ProductStatus.in_stock,
        stock_quantity=3
    )
    db.add(product_to_delete)
    db.commit()

    product_in_db = db.query(Product).filter(Product.id == 1).first()
    assert product_in_db is not None, "Produto não foi adicionado corretamente"

    response = del_product(db, product_id=1)

    assert response.status_code == 200

    response_data = json.loads(response.body.decode())

    assert response_data == {"message": "Item excluído com sucesso!"}

    deleted_product = db.query(Product).filter(Product.id == 1).first()
    assert deleted_product is None, "Produto não foi excluído corretamente"
