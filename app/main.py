from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.v1.routes import router
import os

app = FastAPI()
app.include_router(router)

# URL do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/products_crud_api.db"

# Criação do diretório do banco de dados, caso não exista
os.makedirs(os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

# Cria as tabelas no banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)
