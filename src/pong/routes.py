from aiohttp import web
from .handlers import websocket_handler, landing_handler


#routing config for the application
routes = [
    web.get("/", landing_handler),
    web.get("/ws", websocket_handler),
]
