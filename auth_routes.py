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

@auth_router.get("/", tags=["auth"])
async def autenticar():
    return {"message": "Hello World"}


@auth_router.post("/criar-usuario", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Agora acessamos via usuario.email, usuario.senha, etc.
    usuario_existente = db.query(User).filter(User.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao cadastrar usuário: Email já cadastrado"
        )
    
    # Gerando o hash da senha
    senhaCripto = bcrypt_context.hash(usuario.senha)
    
    novo_usuario = User(nome=usuario.nome, email=usuario.email, senha=senhaCripto)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"message": "Usuário criado com sucesso",
            "usuario": {"nome": novo_usuario.nome, "email": novo_usuario.email}}
