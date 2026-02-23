from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import BaseModel
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EMPIRE_MINUTES, SECRET_KEY
from models import User
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


# Definindo um modelo Pydantic para receber os dados com segurança no corpo da requisição
class UsuarioCreate(BaseModel):
    email: str
    senha: str
    nome: str


class UsuarioLogin(BaseModel):
    email: str
    senha: str


def criar_token(id, duracao_token=timedelta(minutes=float(ACCESS_TOKEN_EMPIRE_MINUTES))):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id), "exp": data_expiracao.timestamp()}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


async def verificar_token(token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
        return user
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def autenticar_usuario(email, senha, db):
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario


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
    usuario = autenticar_usuario(usuario_login.email, usuario_login.senha, db)
    if not usuario:
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao fazer login, usuário não existente"
        )
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}


@auth_router.get("/refresh", tags=["auth"])
async def user_refresh_token(user: User = Depends(verificar_token)):
    access_token = criar_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
