from fastapi import FastAPI
from .database import Base, engine
from routes import router

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app.include_router(router)
