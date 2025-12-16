import os
import json
import time
import random
from datetime import datetime, timezone

from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_raw")
INTERVAL = float(os.getenv("PRODUCE_INTERVAL_SECONDS", "2"))
SENSOR_COUNT = int(os.getenv("SENSOR_COUNT", "5"))


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def generate_message(sensor_id: int) -> dict:
    return {
        "sensor_id": f"sensor-{sensor_id}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(18.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 80.0), 2),
    }


def main():
    producer = create_producer()
    print(f"[sensor-simulator] Producing to {KAFKA_BOOTSTRAP_SERVERS}/{KAFKA_TOPIC}")

    while True:
        for sid in range(1, SENSOR_COUNT + 1):
            msg = generate_message(sid)
            producer.send(KAFKA_TOPIC, msg)
            print("[sensor-simulator] Produced:", msg)
        producer.flush()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
