import asyncio
import aiohttp
import json


async def session_handler(client1, client2):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(sync_events(client1, client2)),
        loop.create_task(sync_events(client2, client1)),
    ]

    await asyncio.wait(*tasks)


async def sync_events(sender, reciever):
    loop = asyncio.get_event_loop()

    async for msg in sender:
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                event = json.loads(msg.data)["event"]
            except:
                continue
            loop.create_task(reciever.send_json({"event": event}))

        elif msg.type == aiohttp.WSMsgType.ERROR:
            loop.create_task(reciever.send_json({"event": "ws_error"}))
