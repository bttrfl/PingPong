import asyncio
import aiohttp
import json


#handles game session
async def session_handler(client1, client2):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(sync_events(client1, client2)),
        loop.create_task(sync_events(client2, client1)),
    ]

    await asyncio.wait(*tasks)


#syncs events between to clients in game session
async def sync_events(sender, reciever):
    loop = asyncio.get_event_loop()

    async for msg in sender:
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                event = json.loads(msg.data)["event"]
            except:

                #if we couldn't decode message, we just skip it
                continue

            #don't wait for response, just create a background task
            loop.create_task(reciever.send_json({"event": event}))

        #spwcial event is sent in case of ws error
        elif msg.type == aiohttp.WSMsgType.ERROR:
            loop.create_task(reciever.send_json({"event": "ws_error"}))
