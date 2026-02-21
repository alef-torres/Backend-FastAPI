from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from sqlalchemy.orm import Session
from database import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/", tags=["auth"])
async def autenticar():
    return {"message": "Hello World"}


@auth_router.post("/criar-usuario", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def criar_usuario(email: str, senha: str, nome: str, db: Session = Depends(get_db)):
    usuario_existente = db.query(User).filter(User.email == email).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao cadastrar usuário: Email já cadastrado"
        )
    
    novo_usuario = User(nome=nome, email=email, senha=senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"message": "Usuário criado com sucesso", "usuario": {"nome": novo_usuario.nome, "email": novo_usuario.email}}