FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY migrations ./migrations
COPY wait-for-postgres.py .

# Set environment variable for port
ENV PORT=8000

# Use the wait script to ensure Postgres is ready before starting uvicorn
CMD ["python3", "./wait-for-postgres.py"]
