import asyncio
import aiohttp
import json


#handles game sessions
async def session_handler(client1, client2):
    await start_game(client1, client2)
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(sync_events(client1, client2)),
        loop.create_task(sync_events(client2, client1)),
    ]

    await asyncio.wait(tasks)


#sends events. indicating the game is ready to begin
async def start_game(client1, client2):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(client1.send_json({"event": "gameReady"})),
        loop.create_task(client2.send_json({"event": "gameReady"})),
    ]
    await asyncio.wait(tasks)


#syncs events between two clients in a game session
async def sync_events(sender, reciever):
    loop = asyncio.get_event_loop()

    async for msg in sender:
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                event = json.loads(msg.data)["event"]
            except:

                #if we couldn't decode message, we drop it
                continue

            #don't wait for response, just create a background task
            loop.create_task(reciever.send_json({"event": event}))

        #special event is sent in case of ws error
        elif msg.type == aiohttp.WSMsgType.ERROR:
            loop.create_task(reciever.send_json({"event": "wsError"}))
