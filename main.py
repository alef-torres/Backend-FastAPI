import os

from fastapi import FastAPI
from database import engine, Base
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EMPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EMPIRE_MINUTES")

# Cria as tabelas no banco de dados se elas não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(order_router)
app.include_router(auth_router)
# uvicorn main:app --reload
