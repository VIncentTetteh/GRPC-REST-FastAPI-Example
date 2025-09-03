import uvicorn
import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .rest_api import router
from .grpc_server import TodoService
from .generated import todo_pb2_grpc,todo_pb2
from .db import engine, Base
import grpc_reflection.v1alpha.reflection as grpc_reflection



@asynccontextmanager
async def lifespan(app: FastAPI):
    # init DB
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # create gRPC server in the same loop
    grpc_server = grpc.aio.server()
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), grpc_server)
    grpc_server.add_insecure_port("[::]:50052")
    SERVICE_NAMES = (
        todo_pb2.DESCRIPTOR.services_by_name['TodoService'].full_name,
        grpc_reflection.SERVICE_NAME,
    )
    grpc_reflection.enable_server_reflection(SERVICE_NAMES, grpc_server)
    await grpc_server.start()
    print("✅ gRPC server started on :50052")

    try:
        yield   # hand control back to FastAPI
    finally:
        await grpc_server.stop(0)
        print("🛑 gRPC server stopped")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


