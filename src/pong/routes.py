from aiohttp import web
from .handlers import *


#routing setup for the application
routes = [
    web.get("/", landing_handler),
    web.get("/ws/game", game_handler),
    web.get("/leaderboard/show", show_leaderboard),
    web.post("/user/login", login_handler),
    web.post("/user/signup", signup_handler),
    web.get("/user/logout", logout_handler),
]
