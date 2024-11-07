from sqlalchemy import Column, Integer, String, Float, Enum
from app.db.database import Base
import enum

class ProductStatus(enum.IntEnum):
    """Define os possíveis status de um produto."""
    in_stock = 1
    replenishment = 2
    out_of_stock = 3

class Product(Base):
    """Modelo para a tabela de produtos."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
