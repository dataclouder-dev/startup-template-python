FROM python:3.12.7-slim-bookworm as builder

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "app.main:app"]
