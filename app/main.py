from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.v1.routes import router
import os

app = FastAPI()
app.include_router(router)

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/products_crud_api.db"

os.makedirs(os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

Base.metadata.create_all(bind=engine)
