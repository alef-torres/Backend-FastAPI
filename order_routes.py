from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/", tags=["order"])
async def pedidos():
    return {"message": "Hello World"}