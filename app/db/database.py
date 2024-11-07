import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pymongo import MongoClient

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./products_crud_api.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = MongoClient(MONGO_DETAILS)

database = client["products_logs"]
views_collection = database["product_views"]

def get_db():
    """Cria uma nova sessão de banco de dados e garante seu fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
