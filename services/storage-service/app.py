import os
import json
import psycopg2
from kafka import KafkaConsumer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "sensor_agg")

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "metrics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")


def save_to_db(cursor, msg):
    """Speichert aggregierte Sensordaten in PostgreSQL."""
    query = """
    INSERT INTO sensor_metrics (timestamp, avg_temperature, avg_humidity, count)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        msg["timestamp"],
        msg["avg_temperature"],
        msg["avg_humidity"],
        msg["count"]
    ))


def main():
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="storage-group",
    )

    print("[storage-service] Connecting to PostgreSQL...")

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    print(f"[storage-service] Writing messages from {INPUT_TOPIC} into DB")

    for message in consumer:
        value = message.value
        save_to_db(cursor, value)
        print("[storage-service] Saved:", value)


if __name__ == "__main__":
    main()
