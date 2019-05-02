import asyncio
import aiohttp
from .session import session_handler
from aiohttp import web
import aiohttp_jinja2


__all__ = [
    "game_handler",
    "landing_handler",
    "show_leaderboard",
    "update_leaderboard",
    "login_handler",
    "logout_handler",
]

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
async def game_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    c = Client(ws)
    await queue.put(c)
    await c.wait_finished()
    return ws


#a handler for the main page
@aiohttp_jinja2.template('index.html')
async def landing_handler(request):
    return {}


#returns a json serialized leaderboard data from database
async def show_leaderboard(request):
    pass


#updates winrate for a specific user
@session_middleware
async def update_leaderboard(request):
    pass


#auth handlers
@session_middleware
async def logout_handler(request):
    pass


@session_middleware
async def login_handelr(request):
    pass


#background tasks
async def start_background_tasks(app):
    app['matchmaker'] = app.loop.create_task(matchmaker(queue))


async def cleanup_background_tasks(app):
    app['matchmaker'].cancel()
    await app['matchmaker']
