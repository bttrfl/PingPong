import asyncio
import aiohttp
import session
from aiohttp import web


app = web.Application()

queue = asyncio.Queue()


async def matchmaker(queue):
    while True:
        conn1 = await queue.get()
        conn2 = await queue.get()
        ioloop = asyncio.get_event_loop()
        ioloop.create_task(session.handler(conn1, conn2))
   
    
async def websocket_handler(request):
    print("kek2")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await queue.put(ws)
    return ws


async def start_background_tasks(app):
    app['matchmaker'] = app.loop.create_task(matchmaker(queue))


async def cleanup_background_tasks(app):
    app['matchmaker'].cancel()
    await app['matchmaker']


async def landing_handler(request):
    index = open('../../static/html/page.html')
    return web.Response(body=index.read().encode('utf-8'), content_type='text/html')


app.add_routes([web.get('/ws', websocket_handler),
                web.get('/', landing_handler)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)

