import os
import json
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
from statistics import mean

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
INPUT_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "sensor_clean")
OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "sensor_agg")

WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", "5"))  # Anzahl Messages pro Aggregation


def aggregate_window(messages):
    """Berechnet Durchschnittswerte aus einer Fenstergruppe."""
    temps = [m["temperature"] for m in messages]
    hums = [m["humidity"] for m in messages]

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "avg_temperature": round(mean(temps), 2),
        "avg_humidity": round(mean(hums), 2),
        "count": len(messages),
    }


def main():
    consumer = KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="stream-group",
    )

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    buffer = []

    print(f"[stream-processing] Aggregating every {WINDOW_SIZE} messages")

    for message in consumer:
        msg = message.value
        buffer.append(msg)

        if len(buffer) >= WINDOW_SIZE:
            agg = aggregate_window(buffer)
            producer.send(OUTPUT_TOPIC, agg)
            print("[stream-processing] Published aggregate:", agg)
            buffer = []


if __name__ == "__main__":
    main()
