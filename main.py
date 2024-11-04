from fastapi import FastAPI
from database import Base, engine
from routes import router

app = FastAPI()

app.include_router(router)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


