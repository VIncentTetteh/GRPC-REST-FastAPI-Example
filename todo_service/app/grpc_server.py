import grpc
from .generated import todo_pb2, todo_pb2_grpc, user_pb2, user_pb2_grpc
from .db import AsyncSessionLocal as SessionLocal
from . import crud

async def get_user(user_id: int):
    """Calls UserService via gRPC to check if user exists"""
    async with grpc.aio.insecure_channel("user_service:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        try:
            response = await stub.GetUser(user_pb2.GetUserRequest(id=user_id))
            if response.id:
                return response
        except grpc.aio.AioRpcError:
            return None
    return None

class TodoService(todo_pb2_grpc.TodoServiceServicer):
    async def CreateTodo(self, request, context):
        user = await get_user(request.user_id)
        if not user:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid user_id")
            return todo_pb2.TodoResponse()

        async with SessionLocal() as db:
            todo = await crud.create_todo(db, request.title, request.description, request.user_id)
            return todo_pb2.TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                user_id=todo.user_id
            )

    async def GetTodo(self, request, context):
        async with SessionLocal() as db:
            todo = await crud.get_todo(db, request.id)
            if not todo:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Todo not found")
                return todo_pb2.TodoResponse()
            return todo_pb2.TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                user_id=todo.user_id
            )
