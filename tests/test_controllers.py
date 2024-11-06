import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Product
from app.controllers.controllers import post_product, get_all_products, put_product
from app.schemas.schemas import ProductCreate, ProductUpdate, ProductStatus

# Adicionando o diretório 'app' ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app')))

# Configuração do banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"

# Criar o engine de testes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar a sessão do banco de dados para testes
@pytest.fixture(scope="module")
def db():
    # Criar as tabelas
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

# Criar um produto para usar nas funções de teste
@pytest.fixture
def product(db):
    # Criando um produto
    product = Product(id=1, name="Produto Teste", description="Descrição do produto", price=100.0, status=ProductStatus.in_stock, stock_quantity=10)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# Teste para a função post_product
def test_post_product(db):
    # Gerar um UUID para o produto
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

