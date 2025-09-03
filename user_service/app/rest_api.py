from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from . import crud

router = APIRouter()

@router.post("/users")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, name, email)

@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        return {"error": "User not found"}
    return user
