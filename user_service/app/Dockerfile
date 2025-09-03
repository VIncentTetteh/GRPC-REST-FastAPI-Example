FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . ./user_service

EXPOSE 8000 50051

CMD ["uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
