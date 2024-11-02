from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# Configuração do SQLite com SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./products_crud_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuração do MongoDB com pymongo
MONGO_DETAILS = "mongodb://localhost:27017"
client = MongoClient(MONGO_DETAILS)

# Banco de dados MongoDB
database = client.products_logs
views_collection = database.product_views
