from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional, List
from enum import IntEnum
from datetime import datetime

class ProductStatus(IntEnum):
    """Define os possíveis status de um produto."""
    in_stock = 1
    replenishment = 2
    out_of_stock = 3

class ProductBase(BaseModel):
    """Modelo base para o produto, utilizado em criação, atualização e resposta."""
    name: str = Field(..., title="Nome do Produto", max_length=100)
    description: Optional[str] = Field(None, title="Descrição do Produto")
    price: Annotated[float, Field(..., gt=0, title="Preço do Produto")]
    status: Optional[ProductStatus] = Field(None, exclude=True, title="Status do Produto")
    stock_quantity: Optional[Annotated[int, Field(..., ge=0, exclude=True, title="Quantidade em Estoque")]] = Field(exclude=True)

    @field_validator('name')
    def validate_name(cls, value):
        if not value:
            raise ValueError("O campo 'name' é obrigatório.")
        if len(value) > 100:
            raise ValueError("O campo 'name' não pode ter mais que 100 caracteres.")
        return value

    @field_validator('description')
    def validate_description(cls, value):
        if value and len(value) > 200:
            raise ValueError("O campo 'description' não pode ter mais que 200 caracteres.")
        return value

    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("O campo 'price' deve ser maior que zero.")
        return value

    @field_validator('status')
    def validate_status(cls, value):
        if isinstance(value, str):
            status_mapping = {
                "in_stock": ProductStatus.in_stock,
                "replenishment": ProductStatus.replenishment,
                "out_of_stock": ProductStatus.out_of_stock
            }
            if value not in status_mapping:
                raise ValueError("O campo 'status' deve ser 'in_stock', 'replenishment' ou 'out_of_stock'.")
            return status_mapping[value]
        return value

    @field_validator('stock_quantity')
    def validate_stock_quantity(cls, value):
        if value is not None and value < 0:
            raise ValueError("O campo 'stock_quantity' deve ser maior ou igual a zero.")
        return value

    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(ProductBase):
    pass

class ProductLog(BaseModel):
    searched_at: datetime 

class ProductWithLogs(BaseModel):
    id: int
    name: str
    description: str
    price: float
    logs: List[ProductLog]
