import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do SQLite com SQLAlchemy
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./products_crud_api.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuração do MongoDB com pymongo
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_DETAILS)

# Banco de dados MongoDB
database = client["products_logs"]
views_collection = database["product_views"]

# Função para obter uma sessão do banco de dados SQLite
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
