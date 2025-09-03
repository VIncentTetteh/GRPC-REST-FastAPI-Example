FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . ./todo_service

EXPOSE 8001 50052

CMD ["uvicorn", "todo_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
