from fastapi import FastAPI
from database import engine, Base
from passlib.context import CryptContext

# Cria as tabelas no banco de dados se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(order_router)
app.include_router(auth_router)
# uvicorn main:app --reload
