import os
import psycopg2
from fastapi import FastAPI
from fastapi.responses import JSONResponse

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "metrics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

app = FastAPI(title="Sensor Metrics API")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


@app.get("/metrics/latest")
def get_latest_metrics():
    """Liefert den letzten aggregierten Datensatz zurück."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT timestamp, avg_temperature, avg_humidity, count
    FROM sensor_metrics
    ORDER BY id DESC
    LIMIT 1;
    """

    cursor.execute(query)
    row = cursor.fetchone()

    conn.close()

    if not row:
        return JSONResponse(content={"error": "No data available"}, status_code=404)

    return {
        "timestamp": row[0].isoformat(),
        "avg_temperature": row[1],
        "avg_humidity": row[2],
        "count": row[3],
    }


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "API is running"}
