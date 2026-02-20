from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/", tags=["order"])
async def root():
    return {"message": "Hello World"}