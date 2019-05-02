import asyncio
import aiohttp
from .session import session_handler
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session, new_session
import json
import hashlib


__all__ = [
    "game_handler",
    "landing_handler",
    "show_leaderboard",
    "login_handler",
    "signup_handler",
    "logout_handler",
]

#a queue for incoming ws clients(game oponents)
#TODO use a priority queue to match players with similar winrate/rating
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
        c1 = await queue.get()
        c2 = await queue.get()
        loop = asyncio.get_event_loop()
        loop.create_task(session_handler(c1, c2))


#returns a json serialized leaderboard data from database
async def show_leaderboard(request):
    query = "SELECT * from leaderboard ORDER BY winrate DESC LIMIT 100"
    db = request.app.db
    async with db.cursor() as cur:
        await cur.execute(query)
        data = await cursor.fetchall()

    json = json.dumps({"data": data})
    return web.Response(text=json, content_type="application/json")


#auth handlers
async def signup_handler(request):
    data = await request.post()

    #we first check if this user already exists in database
    try:
        uid = await get_uid(request, data)
    except KeyError:
        return web.Response(status=400, body=b'Username or password is missing')
    if uid != None:
        return web.Response(status=401, body=b'User already exists')

    #add a new user to the database
    query = "INSERT INTO users_auth (name, password) VALUES (%(user)s, %(pwd)s)"
    db = request.app.db
    async with db.cursor() as cur:
        #TODO use salt for password hashing
        await cur.execute(query, {"user": data["user"], "pwd": sha256_hex(data["pwd"])})

    await create_session(request, uid)
    return web.Response(body=b'OK')


async def login_handler(request):
    session = await get_session(request)
    if not session.new:
        return web.Response(status=401, body=b'User is already logged in')

    data = await request.post()
    try:
        uid = await get_uid(request, data)
    except KeyError:
        return web.Response(status=400, body=b'Username or password is missing')

    #user not found
    if uid == None:
        return web.Response(status=401, body=b'No such user')

    await create_session(request, uid)
    return web.Response(body=b'OK')


async def create_session(request, uid):
    session = await new_session(request)
    session["uid"] = uid


#gets userid from a database for a given username and password
async def get_uid(request, form_data):
    user = form_data["user"]
    pwd = form_data["pwd"]

    query = "SELECT id FROM users_auth WHERE name=%(user)s AND password=%(pwd)s"
    db = request.app.db
    async with db.cursor() as cur:
        #TODO use salt for password hashing
        await cur.execute(query, {"user": user, "pwd": sha256_hex(pwd)})
        res = await cur.fetchone()

    return res[0] if res != None else None

#returns a hex digest of a sha256 hash of a given string
def sha256_hex(s):
    m = hashlib.sha256()
    m.update(s.encode())
    return m.hexdigest()


async def logout_handler(request):
    session = await get_session(request)
    if session.new:
        return web.Response(status=400, body=b'User is not logged in')
    session.invalidate()
    return web.Response(body=b'OK')


#background tasks
async def start_background_tasks(app):
    app['matchmaker'] = app.loop.create_task(matchmaker(oponent_queue))


async def cleanup_background_tasks(app):
    app['matchmaker'].cancel()
    await app['matchmaker']
