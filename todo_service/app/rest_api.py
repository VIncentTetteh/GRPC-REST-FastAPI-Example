from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from . import crud
import grpc
from .generated import user_pb2, user_pb2_grpc

router = APIRouter()

async def check_user(user_id: int):
    async with grpc.aio.insecure_channel("user_service:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        try:
            response = await stub.GetUser(user_pb2.GetUserRequest(id=user_id))
            if response.id:
                return response
        except grpc.aio.AioRpcError:
            return None
    return None

@router.post("/todos")
async def create_todo(title: str, description: str, user_id: int, db: AsyncSession = Depends(get_db)):
    user = await check_user(user_id)
    if not user:
        return {"error": "Invalid user_id"}
    todo = await crud.create_todo(db, title, description, user_id)
    return todo

@router.get("/todos/{todo_id}")
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo(db, todo_id)
    if not todo:
        return {"error": "Todo not found"}
    return todo
