from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from auth_routes import verificar_token

from models import Order, User

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])


@order_router.get("/", tags=["order"])
async def pedidos():
    return {"message": "Hello World"}


class PedidoCreate(BaseModel):
    id_usuario: int


@order_router.post("/criar-pedido", tags=["order"])
async def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Order(pedido.id_usuario)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido criado com sucesso", "pedido_id": novo_pedido.id}


@order_router.post(f"/cancelar-pedido/{id_pedido}", tags=["order"])
async def cancelar_pedido(id_pedido: int, db: Session = Depends(get_db), user: User = Depends(verificar_token)):
    pedido = db.query(Order).filter(Order.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin or user.id != pedido.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    pedido.status = "CANCELADO"
    db.commit()
    return {}


