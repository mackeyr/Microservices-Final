from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from kafka import KafkaConsumer
import json
import asyncio

router = APIRouter(prefix="/live")

@router.get("/facts/stream")
async def stream_facts():
    consumer = KafkaConsumer(
        "fact-events",
        bootstrap_servers="kafka:9092",
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="browser-consumer"
    )

    async def event_generator():
        loop = asyncio.get_event_loop()
        while True:
            msg = await loop.run_in_executor(None, consumer.poll, 1.0)
            for records in msg.values():
                for record in records:
                    yield f"data: {json.dumps(record.value)}\n\n"
            await asyncio.sleep(0.1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
