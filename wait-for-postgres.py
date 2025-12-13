#!/usr/bin/env python3
import os
import time
import psycopg2
from urllib.parse import urlparse

database_url = os.environ.get("DATABASE_URL", "postgresql://ffuser:ffpass@db:5432/funfacts")

while True:
    try:
        result = urlparse(database_url)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        conn.close()
        print("Postgres is up - continuing")
        break
    except Exception:
        print("Postgres is unavailable - sleeping")
        time.sleep(1)

# Execute command
os.execvp("uvicorn", ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
