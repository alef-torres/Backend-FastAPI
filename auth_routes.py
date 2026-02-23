from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from main import bcrypt_context
from models import User
from sqlalchemy.orm import Session
from database import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Definindo um modelo Pydantic para receber os dados com segurança no corpo da requisição
class UsuarioCreate(BaseModel):
    email: str
    senha: str
    nome: str


class UsuarioLogin(BaseModel):
    email: str
    senha: str


def criar_token(id):
    token = f"jfiejfiajefjf{id}"
    return token


@auth_router.get("/", tags=["auth"])
async def autenticar():
    return {"message": "Hello World"}


@auth_router.post("/criar-usuario", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def criar_usuario(usuario_create: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == usuario_create.email).first()

    if usuario_existente:
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao cadastrar usuário: Email já cadastrado"
        )

    # Gerando o hash da senha
    senhaCripto = bcrypt_context.hash(usuario_create.senha)

    novo_usuario = User(nome=usuario_create.nome, email=usuario_create.email, senha=senhaCripto)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"message": "Usuário criado com sucesso",
            "usuario": {"nome": novo_usuario.nome, "email": novo_usuario.email}}


@auth_router.post("/login", status_code=status.HTTP_200_OK, tags=["auth"])
async def login(usuario_login: UsuarioLogin, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == usuario_login.email).first()

    if not usuario_existente:
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao fazer login, usuário não existente"
        )
    else:
        access_token = criar_token(usuario_login.id)
        return {"access_token": access_token, "token_type": "bearer"}
