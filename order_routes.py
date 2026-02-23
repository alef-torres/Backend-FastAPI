from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel

from models import Order

order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.get("/", tags=["order"])
async def pedidos():
    return {"message": "Hello World"}


class PedidoCreate(BaseModel):
    id_usuario: int


@order_router.post("/pedido", tags=["order"])
async def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Order(pedido.id_usuario)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido criado com sucesso", "pedido_id": novo_pedido.id}
