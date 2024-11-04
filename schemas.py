from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum
from typing import Optional

# Enumeração para os status de um produto
class ProductStatus(str, Enum):
    in_stock = "em estoque"
    replenishment = "em reposição"
    out_of_stock = "em falta"

# Classe base para produtos
class ProductBase(BaseModel):
    id: int
    name: str = Field(..., title="Nome do Produto", max_length=100)
    description: Optional[str] = Field(None, title="Descrição do Produto")
    price: Annotated[float, Field(gt=0, title="Preço do Produto")]
    status: Optional[ProductStatus] = Field(None, title="Status do Produto")
    stock_quantity: Optional[Annotated[int, Field(ge=0, title="Quantidade em Estoque")]] = Field(None)

    class Config:
        model_config = {"from_attributes": True}

# Classe para criar um novo produto
class ProductCreate(ProductBase):
    pass

# Classe para representar a resposta do produto
class ProductResponse(ProductBase):
    id: int

# Classe para atualizar um produto
class ProductUpdate(ProductBase):
    pass
