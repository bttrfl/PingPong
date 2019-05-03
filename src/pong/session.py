import asyncio
from aiostream import stream
import aiohttp
import json
from .client import EVT_READY, EVT_ERROR


#handles game sessions
async def session_handler(client1, client2):
    await start_game(client1, client2)
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(sync_events(client1, client2)),
    ]

    await asyncio.wait(tasks)
    client1.set_finished()
    client2.set_finished()


#sends events indicating the game is ready to begin
async def start_game(client1, client2):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(client1.notify(EVT_READY, 0)),
        loop.create_task(client2.notify(EVT_READY, 1)),
    ]
    await asyncio.wait(tasks)


#syncs events between two clients in a game session
async def sync_events(client1, client2):
    loop = asyncio.get_event_loop()


    async for msg in stream.merge(client1.ws, client2.ws):
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                event = json.loads(msg.data)["event"]
                pos = json.loads(msg.data)["pos"]
            except:

                #if we couldn't decode message, we drop it
                continue

            #don't wait for response, just create a background task
            loop.create_task(client1.notify(event, pos))
            loop.create_task(client2.notify(event, pos))

        #special event is sent in case of ws error
        elif msg.type == aiohttp.WSMsgType.ERROR:
            loop.create_task(client1.notify(EVT_ERROR, pos))
            loop.create_task(client2.notify(EVY_ERROR, pos))
