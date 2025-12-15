from kafka import KafkaConsumer
import json
import time

while True:
    try:
        consumer = KafkaConsumer(
            "fact-events",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id="fact-consumer-group"
        )
        print("Kafka consumer connected")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

while True:
    try:
        for message in consumer:
            print("Received:", message.value)
    except Exception as e:
        print("Consumer error, retrying...", e)
        time.sleep(5)
