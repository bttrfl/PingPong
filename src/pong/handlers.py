import asyncio
import aiohttp
from .session import session_handler
from aiohttp import web

#a queue for incoming ws clients(game oponents)
queue = asyncio.Queue()


#client queue consumer, responsible for matching oponents.
#takes two connections from the queue and passes them to the game session handler
async def matchmaker(queue):
    while True:
        conn1 = await queue.get()
        conn2 = await queue.get()
        ioloop = asyncio.get_event_loop()
        ioloop.create_task(session_handler(conn1, conn2))


#accepts ws clients and puts them in the oponent queue
async def websocket_handler(request):
    print("kek2")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await queue.put(ws)
    return ws


#a handler for the landing page
async def landing_handler(request):
    pass


async def start_background_tasks(app):
    app['matchmaker'] = app.loop.create_task(matchmaker(queue))


async def cleanup_background_tasks(app):
    app['matchmaker'].cancel()
    await app['matchmaker']

