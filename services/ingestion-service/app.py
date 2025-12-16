import os
import json
from kafka import KafkaConsumer, KafkaProducer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "sensor_raw")
OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "sensor_clean")


def is_valid(msg: dict) -> bool:
    """Einfache Plausibilitätsprüfung der Sensordaten."""
    required = ["sensor_id", "timestamp", "temperature", "humidity"]
    if not all(k in msg for k in required):
        return False

    try:
        temp = float(msg["temperature"])
        hum = float(msg["humidity"])
    except (ValueError, TypeError):
        return False

    # Beispielgrenzen – du kannst sie im Bericht erwähnen
    if not ( -20.0 <= temp <= 60.0 ):
        return False
    if not ( 0.0 <= hum <= 100.0 ):
        return False

    return True


def main():
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="ingestion-group",
    )

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print(f"[ingestion-service] Reading from {INPUT_TOPIC}, writing to {OUTPUT_TOPIC}")

    for message in consumer:
        value = message.value
        if is_valid(value):
            producer.send(OUTPUT_TOPIC, value)
            print("[ingestion-service] Forwarded valid message:", value)
        else:
            # Hier könnte man später eine Dead-Letter-Queue einbauen
            print("[ingestion-service] Invalid message dropped:", value)


if __name__ == "__main__":
    main()
