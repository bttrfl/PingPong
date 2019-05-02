import asyncio
import aiohttp
from .session import session_handler
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session, new_session, invalidate, set_new_identity


__all__ = [
    "game_handler",
    "landing_handler",
    "show_leaderboard",
    "login_handler",
    "logout_handler",
]

#a queue for incoming ws clients(game oponents)
oponent_queue = asyncio.Queue()


#a handler for the main page
@aiohttp_jinja2.template('index.html')
async def landing_handler(request):
    session = await get_session(request)
    return {}


#accepts ws clients and puts them in the oponent queue
async def game_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    c = Client(ws)
    await oponent_queue.put(c)
    await c.wait_finished()
    return ws


#client queue consumer, responsible for matching oponents.
#takes two connections from the queue and passes them to the game session handler
async def matchmaker(queue):
    while True:
        c1 = await oponent_queue.get()
        c2 = await oponent_queue.get()
        loop = asyncio.get_event_loop()
        loop.create_task(session_handler(c1, c2))


#returns a json serialized leaderboard data from database
async def show_leaderboard(request):
    pass


#auth handlers
async def signup_handler(request):
    pass

async def login_handler(request):
    data = await request.post()
    try:
        user = data["user"]
        pwd = data["pwd"]
    except KeyError:
        return web.Response(status=400, text="Bad request")

    query = "SELECT id FROM users_auth WHERE name=%(user)s, AND password=%(pwd)s"
    db = request.app.db
    async with db.cursor() as cur:
        await cur.execute(query, {"user": uname, "pwd": pwd})
        (uid,) = await cur.fetchone()

    if uid == None:
        return web.Response(status=403, text="Forbidden")

    session = await new_session(request)
    session.set_new_identity(uid)
    session["user"] = user


async def logout_handler(request):
    session = await get_session(request)
    if not session.new:
        session.invalidate()


#background tasks
async def start_background_tasks(app):
    app['matchmaker'] = app.loop.create_task(matchmaker(queue))


async def cleanup_background_tasks(app):
    app['matchmaker'].cancel()
    await app['matchmaker']
