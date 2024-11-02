from sqlalchemy import Column, Integer, String, Float, Enum
from .database import Base
import enum

# Modelo dos Status dos Produtos
class ProductStatus(str, enum.Enum):
    in_stock = "em estoque"
    replenishment = "em reposição"
    out_of_stock = "em falta"

# Modelo dos Produtos
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), nullable=False)
    stock_quantity = Column(Integer, nullable=False)