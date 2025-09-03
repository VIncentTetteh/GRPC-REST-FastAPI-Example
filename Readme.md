```markdown
# gRPC + FastAPI CRUD Microservices

This project demonstrates a **microservices architecture** using:
- **FastAPI** (for REST endpoints)
- **gRPC** (for internal service-to-service communication)
- **PostgreSQL** (as persistent storage, one DB per service)
- **Docker Compose** (for local orchestration)

We build two services:

- **User Service**  
  - Manages users (`id`, `name`, `email`)  
  - Exposes:
    - REST API for external clients
    - gRPC API for internal calls (used by Todo Service)

- **Todo Service**  
  - Manages todos (`id`, `title`, `description`, `user_id`)  
  - Exposes:
    - REST API for external clients
    - gRPC API for internal calls
  - Validates `user_id` by calling **User Service** via gRPC

---

## 📂 Project Structure

```

grpc-fastapi-crud/
│── docker-compose.yml
│── init.sql
│── user\_service/
│   └── app/
│       ├── main.py
│       ├── rest\_api.py
│       ├── grpc\_server.py
│       ├── crud.py
│       ├── db.py
│       ├── models.py
│       ├── generated/
│       │   ├── user.proto
│       │   ├── user\_pb2.py
│       │   ├── user\_pb2\_grpc.py
│       └── requirements.txt
│
│── todo\_service/
│   └── app/
│       ├── main.py
│       ├── rest\_api.py
│       ├── grpc\_server.py
│       ├── crud.py
│       ├── db.py
│       ├── models.py
│       ├── generated/
│       │   ├── todo.proto
│       │   ├── todo\_pb2.py
│       │   ├── todo\_pb2\_grpc.py
│       │   ├── user\_pb2.py      # copied from user\_service for gRPC stubs
│       │   ├── user\_pb2\_grpc.py
│       └── requirements.txt

````

---

## Running the Project

### 1. Start Services
```bash
docker-compose up --build
````

This launches:

* **Postgres** at `localhost:5432`
* **User Service**

  * REST: `http://localhost:8000`
  * gRPC: `localhost:50051`
* **Todo Service**

  * REST: `http://localhost:8001`
  * gRPC: `localhost:50052`

---

## REST API Examples

### Create User

```bash
curl -X POST "http://localhost:8000/users?name=John&email=john@example.com"
```

### Get User

```bash
curl http://localhost:8000/users/1
```

### Create Todo

```bash
curl -X POST "http://localhost:8001/todos?title=Buy milk&description=2 packs&user_id=1"
```

### Get Todo

```bash
curl http://localhost:8001/todos/1
```

---

## gRPC Examples

We use [`grpcurl`](https://github.com/fullstorydev/grpcurl) for testing.

### List services

```bash
grpcurl -plaintext localhost:50051 list
```

### Create User

```bash
grpcurl -plaintext -d '{"name":"Alice","email":"alice@example.com"}' \
  localhost:50051 user.UserService/CreateUser
```

### Get User

```bash
grpcurl -plaintext -d '{"id":1}' \
  localhost:50051 user.UserService/GetUser
```

### Create Todo

```bash
grpcurl -plaintext -d '{"title":"Read book","description":"Finish chapter 1","user_id":1}' \
  localhost:50052 todo.TodoService/CreateTodo
```

---

## Internal Communication

* `todo_service` **never queries the user database directly**.
* Instead, it calls `user_service` via **gRPC** to check if a `user_id` exists.
* This keeps services isolated and aligned with microservice best practices.

---

## Development

### Regenerate gRPC stubs

If you modify `.proto` files:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto
```

### Run a service locally

```bash
cd user_service/app
uvicorn main:app --reload --port 8000
```

---

## Features

* Async **SQLAlchemy** with Postgres
* **FastAPI** REST + gRPC running in same process
* **Reflection API** enabled for easy grpcurl testing
* Fully containerized with **Docker Compose**
* Service-to-service communication via **gRPC**

