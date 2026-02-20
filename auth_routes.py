from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/", tags=["auth"])
async def autenticar():
    return {"message": "Hello World"}