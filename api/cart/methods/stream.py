import asyncio
import json
from typing import AsyncIterable

from fastapi.responses import StreamingResponse

from api.core.method import Method


class CartStreamMethod(Method):
    async def run(self):
        self.queue = asyncio.Queue()
        self.id = self.agent.subscribe(self.queue)
        return StreamingResponse(self.stream(), media_type="text/event-stream")

    async def stream(self) -> AsyncIterable[str]:
        while True:
            items = await self.queue.get()
            data = json.dumps(
                [
                    {
                        "item_id": item.item_id,
                        "name": item.name,
                        "icon": item.icon,
                        "origin": item.origin
                    }
                    for item in items
                ]
            )
            yield f"event: cart\ndata: {data}\n\n"
