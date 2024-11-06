from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional, List
from enum import IntEnum
from datetime import datetime

# Enumeração para os status de um produto
class ProductStatus(IntEnum):
    in_stock = 1
    replenishment = 2
    out_of_stock = 3

# Classe base para produtos
class ProductBase(BaseModel):
    id: int
    name: str = Field(..., title="Nome do Produto", max_length=100)
    description: Optional[str] = Field(None, title="Descrição do Produto")
    price: Annotated[float, Field(..., gt=0, title="Preço do Produto")]
    status: Optional[ProductStatus] = Field(None, title="Status do Produto")
    stock_quantity: Optional[Annotated[int, Field(..., ge=0, title="Quantidade em Estoque")]] = Field(None)

    @field_validator('status')
    def validate_status(cls, value):
        if isinstance(value, str):
            
            # Mapeia a string para o valor correspondente
            if value == "in_stock":
                return ProductStatus.in_stock
            elif value == "replenishment":
                return ProductStatus.replenishment
            elif value == "out_of_stock":
                return ProductStatus.out_of_stock
            else:
                raise ValueError("Input should be 'in_stock', 'replenishment' or 'out_of_stock'")
        return value

    class Config:
        orm_mode = True

# Classe para criar um novo produto
class ProductCreate(ProductBase):
    pass

# Classe para representar a resposta do produto
class ProductResponse(ProductBase):
    class Config:
        orm_mode = True

# Classe para atualizar um produto
class ProductUpdate(ProductBase):
    pass

# Classe para log de visualizações
class ProductLog(BaseModel):
    searched_at: datetime 

# Classe para produto com logs
class ProductWithLogs(BaseModel):
    id: int
    name: str
    description: str
    price: float
    logs: List[ProductLog]
