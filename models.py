from sqlalchemy import Column, Integer, String, Float
from .database import Base

# Modelo dos Produtos
class Product(Base):
    __tablename__ = "products"
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    status = Column(String, index=True)
    stock_quantity = Column(Integer)