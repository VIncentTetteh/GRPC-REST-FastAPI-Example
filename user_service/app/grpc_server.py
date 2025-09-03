import grpc
from .generated import user_pb2, user_pb2_grpc
from .db import AsyncSessionLocal as SessionLocal
from . import crud

class UserService(user_pb2_grpc.UserServiceServicer):
    async def CreateUser(self, request, context):
        async with SessionLocal() as db:
            user = await crud.create_user(db, request.name, request.email)
            return user_pb2.UserResponse(id=user.id, name=user.name, email=user.email)

    async def GetUser(self, request, context):
        async with SessionLocal() as db:
            user = await crud.get_user(db, request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.UserResponse()
            return user_pb2.UserResponse(id=user.id, name=user.name, email=user.email)
