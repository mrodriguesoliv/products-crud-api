from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

# Enumeração para os status de um produto
class ProductStatus(str, Enum):
    in_stock = "em estoque"
    replenishment = "em reposição"
    out_of_stock = "em falta"

# Usando Annotated para validação
class ProductCreate(BaseModel):
    name: str = Field(..., title="Nome do Produto", max_length=100)
    description: str = Field(None, title="Descrição do Produto")
    price: Annotated[float, Field(gt=0, title="Preço do Produto")]
    status: ProductStatus = Field(..., title="Status do Produto")
    stock_quantity: Annotated[int, Field(ge=0, title="Quantidade em Estoque")]

# Representa a resposta do produto
class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True