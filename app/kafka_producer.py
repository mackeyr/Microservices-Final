from kafka import KafkaProducer
import json
import time

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        while True:
            try:
                _producer = KafkaProducer(
                    bootstrap_servers="kafka:9092",
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                )
                print("Kafka producer connected")
                break
            except Exception as e:
                print("Waiting for Kafka producer...", e)
                time.sleep(5)
    return _producer

def send_fact_created_event(fact):
    producer = get_producer()
    producer.send("fact-events", {
        "event": "fact_created",
        "fact_id": fact.id,
        "text": fact.text
    })

    producer.flush()
