from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from auth_routes import verificar_token

from models import Order, User, ItemOrder

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])


class ItemPedido(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float


@order_router.get("/", tags=["order"])
async def pedidos():
    return {"message": "Hello World"}


@order_router.post("/criar-pedido", tags=["order"])
async def criar_pedido(db: Session = Depends(get_db), user: User = Depends(verificar_token)):
    novo_pedido = Order(user_id=user.id)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido criado com sucesso", "pedido_id": novo_pedido.id}


@order_router.post("/cancelar-pedido/{id_pedido}", tags=["order"])
async def cancelar_pedido(id_pedido: int, db: Session = Depends(get_db), user: User = Depends(verificar_token)):
    pedido = db.query(Order).filter(Order.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not (user.admin or user.id == pedido.user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sem autorização")
    pedido.status = "CANCELADO"
    db.commit()
    return {"message": "Pedido cancelado com sucesso"}


@order_router.get("/listar")
async def listar_pedidos(db: Session = Depends(get_db), user: User = Depends(verificar_token)):
    if user.admin:
        pedidos = db.query(Order).all()
    else:
        pedidos = db.query(Order).filter(Order.user_id == user.id).all()
    return {"pedidos": pedidos}


@order_router.post("/pedido/adicionar/{id_pedido}", tags=["order"])
async def adicionar_item_ao_pedido(id_pedido: int,
                                   item_adicionar: ItemPedido,
                                   db: Session = Depends(get_db),
                                   user: User = Depends(verificar_token)):
    pedido = db.query(Order).filter(Order.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not (user.admin or user.id == pedido.user_id):
        raise HTTPException(status_code=401, detail="Sem autorização")

    item_pedido = ItemOrder(user_id=user.id,
                            flavor=item_adicionar.sabor,
                            quantity=item_adicionar.quantidade,
                            size=item_adicionar.tamanho,
                            price_unit=item_adicionar.preco_unitario,
                            order_id=id_pedido)
    db.add(item_pedido)
    db.commit()
    db.refresh(pedido)
    pedido.calcular_price()
    db.commit()
    return {"mensagem": "Item adicionado com sucesso"}


@order_router.post("/pedido/remover/{id_item_pedido}", tags=["order"])
async def remover_item_ao_pedido(id_item_pedido: int,
                                 db: Session = Depends(get_db),
                                 user: User = Depends(verificar_token)):
    item_pedido = db.query(ItemOrder).filter(ItemOrder.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item não encontrado")

    if not (user.admin or user.id == item_pedido.user_id):
        raise HTTPException(status_code=401, detail="Sem autorização")

    pedido_id = item_pedido.order_id
    db.delete(item_pedido)
    db.commit()

    pedido = db.query(Order).filter(Order.id == pedido_id).first()
    if pedido:
        pedido.calcular_price()
        db.commit()

    return {"mensagem": "Item removido com sucesso"}
