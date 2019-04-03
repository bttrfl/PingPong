import asyncio
import aiohttp
import session
from aiohttp import web


app = web.Application()

queue = asyncio.Queue()


async def merge_queues(common, session):
    print("request merging made")

async def matchmaker(queue):
    ctr = 1
    sess = []
    while True:
        conn = await queue.get()
        if ctr == 2:
            sess.append(conn)
            shared = asyncio.Queue()
            ioloop = asyncio.get_event_loop()
            tasks = [ioloop.create_task(session.handler(sess[0], sess[1]))]
            sess = []
            ctr = 1
        else:
            ctr += 1
            print("appended")
            sess.append(conn)


async def websocket_handler(request):
    print("kek2")
    ws = web.WebSocketResponse()
    await queue.put(ws)
   # await ws.prepare(request)

   # async for msg in ws:
   #     if msg.type == aiohttp.WSMsgType.TEXT:
   #         print(msg.data)
   #         if msg.data == 'close':
   #             await ws.close()
   #         else:
   #             await ws.send_str(msg.data)
   #     elif msg.type == aiohttp.WSMsgType.ERROR:
   #         print('ws connection closed with exception %s' %
   #               ws.exception())
   # print('websocker connection closed')
    return ws


async def start_background_tasks(app):
    app['redis_listener'] = app.loop.create_task(matchmaker(queue))


async def cleanup_background_tasks(app):
    app['redis_listener'].cancel()
    await app['redis_listener']



app.add_routes([web.get('/ws', websocket_handler)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)

